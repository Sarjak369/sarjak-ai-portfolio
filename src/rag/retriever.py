"""
RAG retrieval system using LangChain
"""
import re
from typing import List, Dict, Any, Optional, Tuple
from collections import Counter

from src.rag.data_loader import DataLoader
from src.rag.vectorstore import VectorStoreManager
from src.llm.model import LLMInterface
from src.utils.logger import logger
import config


SENSITIVE_TERMS = [kw.lower() for kw in config.SENSITIVE_KEYWORDS]


class RAGRetriever:
    """LangChain-based RAG system for intelligent query answering"""

    def __init__(self, reset_db: bool = False, llm_provider: Optional[str] = None):
        logger.info("Initializing LangChain RAG system...")
        self.data_loader = DataLoader()
        self.vector_store = VectorStoreManager()
        self.llm = LLMInterface(provider=llm_provider)

        if reset_db:
            self._build_vector_store()
        else:
            try:
                self.vector_store.load_existing()
                stats = self.vector_store.get_stats()
                if stats.get("document_count", 0) == 0:
                    logger.info("Vector store empty, building...")
                    self._build_vector_store()
            except Exception as e:
                logger.info(f"Building new vector store: {e}")
                self._build_vector_store()

        logger.info("✅ LangChain RAG system ready!")

    # -------------------------------------------------------------------------
    # Build / Load
    # -------------------------------------------------------------------------
    def _build_vector_store(self):
        logger.info("Building vector store from data files...")
        documents = self.data_loader.get_all_documents()
        self.vector_store.create_from_documents(documents, reset=False)
        logger.info(f"✅ Vector store built: {self.vector_store.get_stats()}")

    # -------------------------------------------------------------------------
    # Guardrails
    # -------------------------------------------------------------------------
    def _is_sensitive_query(self, q: str) -> bool:
        ql = q.lower()
        if any(term in ql for term in SENSITIVE_TERMS):
            return True
        for _, pattern in config.SENSITIVE_REGEX.items():
            if re.search(pattern, q):
                return True
        return False

    # -------------------------------------------------------------------------
    # Deterministic answer helpers (bypass the LLM for simple facts)
    # -------------------------------------------------------------------------
    def _answer_most_recent(self) -> Optional[str]:
        """Return the most recent experience from experience.json."""
        exp = self.data_loader.experience or {}
        positions = exp.get("positions", [])
        if not positions:
            return None
        latest = positions[0]  # assume newest first in your JSON
        title = latest.get("title", "")
        company = latest.get("company", "")
        duration = latest.get("duration", "")
        location = latest.get("location", "")
        return f"Sarjak’s most recent role is {title} at {company} ({duration}, {location})."

    def _answer_origin(self) -> Optional[str]:
        """
        Prefer hometown for queries like:
        - 'Where is Sarjak from?'
        - 'Which part of India does he come from?'
        Uses profile_context.personal.comes_from_answer if present; otherwise falls back to raised city.
        """
        ctx = self.data_loader.profile_ctx or {}
        personal = ctx.get("personal", {})
        comes_from = (personal.get("comes_from_answer") or "").strip()
        if comes_from:
            return comes_from
        raised = personal.get("raised_in", {}) or {}
        city = (raised.get("city") or "").strip()
        state = (raised.get("state") or "").strip()
        country = (raised.get("country") or "").strip()
        if city and state and country:
            return f"{city}, {state}, {country}"
        if city and state:
            return f"{city}, {state}"
        return None

    def _answer_birth_raised(self) -> Optional[str]:
        """
        Answer 'Where was he born / raised?' from profile_context.personal birth/raised fields.
        """
        ctx = self.data_loader.profile_ctx or {}
        personal = ctx.get("personal", {}) or {}
        b = personal.get("birth", {}) or {}
        r = personal.get("raised_in", {}) or {}
        b_city, b_state, b_country = b.get("city", ""), b.get(
            "state", ""), b.get("country", "")
        r_city, r_state, r_country = r.get("city", ""), r.get(
            "state", ""), r.get("country", "")
        if any([b_city, b_state, b_country]) or any([r_city, r_state, r_country]):
            born_str = ", ".join(
                [x for x in [b_city, b_state, b_country] if x])
            raised_str = ", ".join(
                [x for x in [r_city, r_state, r_country] if x])
            if born_str and raised_str:
                return f"Sarjak was born in {born_str}, and he was raised in {raised_str}."
            if born_str:
                return f"Sarjak was born in {born_str}."
            if raised_str:
                return f"Sarjak was raised in {raised_str}."
        return None

    def _answer_publications(self) -> Optional[str]:
        """
        Summarize publications if present in profile_context.json.
        """
        ctx = self.data_loader.profile_ctx or {}
        pubs = ctx.get("publications", [])
        if not pubs:
            # Some data might be under personal.publications (legacy)
            personal = ctx.get("personal", {}) or {}
            pubs = personal.get("publications", [])
        if not pubs:
            return None

        lines = []
        for p in pubs[:6]:  # cap to keep answers concise
            title = p.get("title", "")
            venue = p.get("venue", p.get("journal", ""))
            date = p.get("date", p.get("year", ""))
            # keep short, link if url present
            if title and (venue or date):
                lines.append(f"• {title} ({venue}, {date})")
            elif title:
                lines.append(f"• {title}")

        if not lines:
            return None

        return "Here are Sarjak’s publications:\n" + "\n".join(lines)

    # -------------------------------------------------------------------------
    # Lightweight rerank (keyword overlap) for retrieved context
    # -------------------------------------------------------------------------
    @staticmethod
    def _keyword_overlap_score(query: str, text: str) -> int:
        q_tokens = [t for t in re.findall(
            r"[A-Za-z0-9]+", query.lower()) if len(t) > 2]
        t_tokens = [t for t in re.findall(
            r"[A-Za-z0-9]+", text.lower()) if len(t) > 2]
        if not q_tokens or not t_tokens:
            return 0
        q_counts = Counter(q_tokens)
        t_counts = Counter(t_tokens)
        # Sum min counts for shared tokens (basic overlap measure)
        score = sum(min(q_counts[w], t_counts[w])
                    for w in q_counts.keys() & t_counts.keys())
        return score

    def _rerank(self, query: str, contexts: List[str], top_n: int = 6) -> List[str]:
        ranked: List[Tuple[int, str]] = []
        for ctx in contexts:
            ranked.append((self._keyword_overlap_score(query, ctx), ctx))
        ranked.sort(key=lambda x: x[0], reverse=True)
        return [c for _, c in ranked[:top_n]]

    # -------------------------------------------------------------------------
    # Retrieve + Answer
    # -------------------------------------------------------------------------
    def retrieve(self, query: str, k: Optional[int] = None) -> List[str]:
        if k is None:
            k = config.RAG_TOP_K
        return self.vector_store.similarity_search(query, k=k)

    def answer_query(self, query: str) -> str:
        logger.info(f"Processing query: {query}")

        # 1) Guardrails
        if self._is_sensitive_query(query):
            return config.SAFE_CONTACT_LINE

        # 2) Shortcut: most recent role
        if any(kw in query.lower() for kw in ["most recent", "latest", "current role", "current job"]):
            ans = self._answer_most_recent()
            if ans:
                return ans

        # 3) Heuristic routing — EDUCATION
        edu_triggers = [
            "undergrad", "undergraduate", "bachelor", "be ", "b.e", "tsec",
            "university of mumbai", "gpa", "grade"
        ]
        if any(t in query.lower() for t in edu_triggers):
            seeded_docs = self.vector_store.similarity_search(
                "education GPA undergraduate bachelor TSEC University of Mumbai",
                k=max(4, config.RAG_TOP_K),
            )
            context_docs = seeded_docs + self.vector_store.similarity_search(
                query, k=config.RAG_TOP_K
            )
        else:
            context_docs = []

        # 4) Heuristic routing — PUBLICATIONS / PAPERS
        pub_triggers = [
            "publication", "publications", "paper", "papers", "research",
            "ieee", "xplore", "humor detection", "mcq", "opencv"
        ]
        if any(t in query.lower() for t in pub_triggers):
            pub_seed = (
                "publications list titles venues dates sarjak maniar ieee xplore "
                "To laugh or not to laugh LSTM humor detection; "
                "Generation and grading of arduous MCQs using NLP and OMR detection using OpenCV"
            )
            pub_docs = self.vector_store.similarity_search(
                pub_seed, k=max(6, config.RAG_TOP_K)
            )
            context_docs = pub_docs + (context_docs or [])  # prepend pubs

        # 5) Default retrieval if no heuristic filled context_docs
        if not context_docs:
            context_docs = self.vector_store.similarity_search(
                query, k=config.RAG_TOP_K)

        # 6) Fall-through to generation
        if not context_docs:
            return "I don’t have enough information to answer that from my records."

        context = "\n\n".join(context_docs)
        return self.llm.generate_with_context(query, context)

    # -------------------------------------------------------------------------
    # Stats
    # -------------------------------------------------------------------------

    def get_stats(self) -> Dict[str, Any]:
        return {
            "vector_store": self.vector_store.get_stats(),
            "llm": self.llm.get_provider_info(),
            "framework": "LangChain"
        }
