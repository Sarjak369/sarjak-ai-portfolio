"""
Load and prepare data for RAG system
"""
from __future__ import annotations
import json
import os

import re
from typing import List, Dict, Any
from pathlib import Path

from PyPDF2 import PdfReader

from src.utils.helpers import load_json
from src.utils.logger import logger
import config


# Optional docs directory ingest (PDF/TXT/MD)
DOCS_DIR = getattr(config, "DOCS_DIR", None)
SUPPORTED_EXTS = {".pdf", ".txt", ".md"}


# ----------------------------------------------------
# Helper: Load JSON from file or environment
# ----------------------------------------------------

def load_json_or_env(path: Path | str, env_key: str) -> dict:
    """
    Load JSON from local file if it exists, otherwise from environment variable.
    """
    # 1️⃣ Try local file (for local dev)
    try:
        if path and Path(path).exists():
            from src.utils.helpers import load_json
            return load_json(path)
    except Exception:
        pass

    # 2️⃣ Try environment variable (for Render)
    data = os.getenv(env_key)
    if data:
        try:
            return json.loads(data)
        except Exception as e:
            logger.warning(f"Failed to parse {env_key}: {e}")

    logger.warning(f"Missing {env_key} and file {path}")
    return {}


class DataLoader:
    """Load and structure portfolio data for RAG"""

    def __init__(self):
        # Core JSON sources (local or env)
        self.profile: Dict[str, Any] = load_json_or_env(
            config.PROFILE_DATA, "PROFILE_JSON")
        self.skills: Dict[str, Any] = load_json_or_env(
            config.SKILLS_DATA, "SKILLS_JSON")
        self.experience: Dict[str, Any] = load_json_or_env(
            config.EXPERIENCE_DATA, "EXPERIENCE_JSON")
        self.projects: Dict[str, Any] = load_json_or_env(
            config.PROJECTS_DATA, "PROJECTS_JSON")
        self.education: Dict[str, Any] = load_json_or_env(
            config.EDUCATION_DATA, "EDUCATION_JSON")

        # Enriched profile context (optional)
        self.profile_ctx: Dict[str, Any] = load_json_or_env(
            getattr(config, "PROFILE_CONTEXT_DATA",
                    config.DATA_DIR / "profile_context.json"),
            "PROFILE_CONTEXT_JSON"
        )

        # Chunking parameters
        self.chunk_size: int = getattr(config, "CHUNK_SIZE", 900)
        self.chunk_overlap: int = getattr(config, "CHUNK_OVERLAP", 120)

        logger.info("Data loader initialized")

    # -----------------------
    # Chunking helpers
    # -----------------------
    def _chunk(self, text: str) -> List[str]:
        """
        Small, safe chunker (character based) with overlap.
        """
        # collapse whitespace a bit to avoid weird spacing from PDFs
        text = re.sub(r"[ \t]+", " ", text)
        text = re.sub(r"\s*\n\s*", "\n", text).strip()

        chunks, i, n = [], 0, len(text)
        step = max(1, self.chunk_size - self.chunk_overlap)
        while i < n:
            chunks.append(text[i: i + self.chunk_size])
            i += step
        return chunks

    # -----------------------
    # Docs/PDF ingestion
    # -----------------------
    def _pdf_to_text(self, path: Path) -> str:
        try:
            reader = PdfReader(str(path))
            pages = [p.extract_text() or "" for p in reader.pages]
            return "\n".join(pages)
        except Exception as e:
            logger.warning(f"PDF read failed for {path.name}: {e}")
            return ""

    def _load_docs_dir(self) -> List[Dict[str, Any]]:
        docs: List[Dict[str, Any]] = []
        if not DOCS_DIR:
            return docs
        dpath = Path(DOCS_DIR)
        if not dpath.exists():
            return docs

        for p in dpath.glob("**/*"):
            if not p.is_file() or p.suffix.lower() not in SUPPORTED_EXTS:
                continue

            if p.suffix.lower() == ".pdf":
                txt = self._pdf_to_text(p)
            else:
                try:
                    txt = p.read_text(encoding="utf-8", errors="ignore")
                except Exception as e:
                    logger.warning(f"Read failed for {p.name}: {e}")
                    continue

            if not txt.strip():
                # index a stub so the filename at least becomes retrievable
                txt = f"Document: {p.stem.replace('_',' ')} ({p.suffix.upper().lstrip('.')})."

            for c in self._chunk(txt):
                docs.append({
                    "content": c,
                    "metadata": {"source": "doc", "file": p.name, "type": "external_doc"}
                })
        return docs

    # -----------------------
    # Enriched profile_context.json → docs
    # -----------------------
    def _context_docs(self) -> List[Dict[str, Any]]:
        docs: List[Dict[str, Any]] = []
        if not self.profile_ctx:
            return docs

        personal = self.profile_ctx.get("personal", {})
        born = personal.get("birth", {})
        raised = personal.get("raised_in", {})
        hobbies = ", ".join(personal.get("hobbies", []))

        # Personal profile (birth, hometown, hobbies)
        personal_txt = (
            "Personal Profile:\n"
            f"Name: {personal.get('full_name','Sarjak Maniar')}\n"
            f"Born: {born.get('city','')}, {born.get('state','')}, {born.get('country','')} "
            f"on {born.get('weekday','')}, {born.get('date_iso','')}\n"
            f"Raised/Hometown: {raised.get('city','')}, {raised.get('state','')}, {raised.get('country','')}\n"
            f"Hobbies: {hobbies}\n"
        )
        for c in self._chunk(personal_txt):
            docs.append({"content": c, "metadata": {
                        "source": "profile_context", "type": "personal"}})

        # Disambiguation for “Where is Sarjak from?”
        comes_from = (personal.get("comes_from_answer") or "").strip()
        if comes_from:
            cf_text = (
                "Disambiguation:\n"
                "If asked 'Where is Sarjak from?' or 'Which part of India does he come from?'\n"
                f"Answer: {comes_from} (he was born in Ahmedabad but raised in Mumbai; prefer hometown for 'from')."
            )
            for c in self._chunk(cf_text):
                docs.append({"content": c, "metadata": {
                            "source": "profile_context", "type": "disambiguation"}})

        # Publications (detailed list under personal.publications)
        pubs_personal = personal.get("publications", [])
        if pubs_personal:
            lines = []
            for i, p in enumerate(pubs_personal, 1):
                lines.append(
                    f"{i}. Title: {p.get('title','')}\n"
                    f"   Year: {p.get('year','')}\n"
                    f"   Venue: {p.get('venue','')}\n"
                    f"   Authors: {', '.join(p.get('authors', []))}\n"
                    f"   Summary: {p.get('summary','')}\n"
                )
            pubs_text = "Publications (Detailed):\n" + "\n".join(lines)
            for c in self._chunk(pubs_text):
                docs.append({"content": c, "metadata": {
                            "source": "profile_context", "type": "publications_detailed"}})

        # Education timeline (compact facts)
        edu_tl = self.profile_ctx.get("education_timeline", [])
        if edu_tl:
            edu_lines = []
            for e in edu_tl:
                edu_lines.append(
                    f"{e.get('level','')}: {e.get('institution','')} "
                    f"({e.get('city','')}, {e.get('country','')}) "
                    f"{e.get('start','')}–{e.get('end','')} "
                    f"GPA/Result: {e.get('gpa', e.get('result',''))}"
                )
            edu_text = "Education Timeline:\n" + "\n".join(edu_lines)
            for c in self._chunk(edu_text):
                docs.append({"content": c, "metadata": {
                            "source": "profile_context", "type": "education_timeline"}})

        # Recency (latest role)
        rec = self.profile_ctx.get("recency", {})
        if rec:
            recent = (
                f"Most recent role: {rec.get('current_role','')} at {rec.get('current_company','')} "
                f"({rec.get('period','')}, {rec.get('location','')})."
            )
            for c in self._chunk(recent):
                docs.append({"content": c, "metadata": {
                            "source": "profile_context", "type": "recency"}})

        # Publications (short list at top-level if present)
        pubs_root = self.profile_ctx.get("publications", [])
        if pubs_root:
            pub_text = "Publications (Summary):\n" + "\n".join(
                f"- {p.get('title','')} ({p.get('venue','')}, {p.get('date','')})"
                for p in pubs_root
            )
            for c in self._chunk(pub_text):
                docs.append({"content": c, "metadata": {
                            "source": "profile_context", "type": "publications"}})

        return docs

    # -----------------------
    # Base JSON → documents
    # -----------------------
    def _base_json_docs(self) -> List[Dict[str, Any]]:
        docs: List[Dict[str, Any]] = []

        # Profile
        if self.profile:
            profile_text = (
                f"Name: {self.profile.get('name','')}\n"
                f"Title: {self.profile.get('title','')}\n"
                f"Bio: {self.profile.get('bio','')}\n"
                f"Location: {self.profile.get('location','')}\n"
                f"Email: {self.profile.get('email','')}\n"
                f"Phone: {self.profile.get('phone','')}\n"
            )
            for c in self._chunk(profile_text):
                docs.append({"content": c, "metadata": {
                            "source": "profile", "type": "personal_info"}})

        # Skills
        if self.skills and "categories" in self.skills:
            for category in self.skills["categories"]:
                skills_text = (
                    f"Skill Category: {category.get('name','')}\n"
                    f"Skills: {', '.join(category.get('skills', []))}\n"
                )
                for c in self._chunk(skills_text):
                    docs.append({"content": c, "metadata": {"source": "skills", "category": category.get(
                        'name', ''), "type": "technical_skills"}})

        # Experience
        if self.experience and "positions" in self.experience:
            for position in self.experience["positions"]:
                highlights = "\n• ".join(position.get("highlights", []))
                exp_text = (
                    f"Position: {position.get('title','')} at {position.get('company','')}\n"
                    f"Duration: {position.get('duration','')}\n"
                    f"Location: {position.get('location','')}\n\n"
                    f"Key Achievements:\n"
                    f"• {highlights}\n\n"
                    f"Technologies: {', '.join(position.get('technologies', []))}\n"
                )
                for c in self._chunk(exp_text):
                    docs.append({"content": c, "metadata": {"source": "experience", "company": position.get(
                        'company', ''), "title": position.get('title', ''), "type": "work_experience"}})

        # Projects
        if self.projects and "projects" in self.projects:
            for project in self.projects["projects"]:
                highlights = "\n• ".join(project.get("highlights", []))
                proj_text = (
                    f"Project: {project.get('name','')}\n"
                    f"Tagline: {project.get('tagline','')}\n\n"
                    f"Description: {project.get('description','')}\n\n"
                    f"Key Features:\n"
                    f"• {highlights}\n\n"
                    f"Technologies: {', '.join(project.get('technologies', []))}\n"
                )
                for c in self._chunk(proj_text):
                    docs.append({"content": c, "metadata": {
                                "source": "projects", "project_name": project.get('name', ''), "type": "project"}})

        # Education
        if self.education and "degrees" in self.education:
            for degree in self.education["degrees"]:
                courses = ", ".join(degree.get("courses", []))
                edu_text = (
                    f"Degree: {degree.get('degree','')}\n"
                    f"Institution: {degree.get('institution','')}\n"
                    f"Duration: {degree.get('duration','')}\n"
                    f"GPA: {degree.get('gpa','')}\n"
                    f"Relevant Courses: {courses}\n"
                )
                for c in self._chunk(edu_text):
                    docs.append({"content": c, "metadata": {"source": "education", "institution": degree.get(
                        'institution', ''), "type": "education"}})

        return docs

    # -----------------------
    # Public API
    # -----------------------
    def get_all_documents(self) -> List[Dict[str, Any]]:
        """
        Convert all data into documents (already chunked) for the vector store.
        """
        documents: List[Dict[str, Any]] = []

        # Base JSON -> docs
        documents.extend(self._base_json_docs())

        # Enriched context (birth/hometown, disambiguation, pubs, timeline, recency)
        documents.extend(self._context_docs())

        # External docs (PDF/TXT/MD)
        documents.extend(self._load_docs_dir())

        logger.info(f"Generated {len(documents)} chunked documents for RAG")
        return documents

    def get_summary(self) -> str:
        """
        A brief summary used elsewhere in the app.
        """
        return (
            f"Portfolio Summary for {self.profile.get('name', 'Sarjak Maniar')}\n"
            f"Professional Title: {self.profile.get('title', 'AI/ML Engineer')}\n"
            f"Experience: {len(self.experience.get('positions', []))} positions | "
            f"Projects: {len(self.projects.get('projects', []))} projects | "
            f"Education: {len(self.education.get('degrees', []))} degrees\n"
            f"Location: {self.profile.get('location', 'Boston, MA')}"
        )
