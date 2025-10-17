"""
Configuration settings for the portfolio application
"""
import os
from pathlib import Path
from dotenv import load_dotenv

# -----------------------------------------------------------------------------
# Load environment variables
# -----------------------------------------------------------------------------
load_dotenv()

# Silence HF tokenizers fork warning (can be overridden via env)
os.environ.setdefault("TOKENIZERS_PARALLELISM", "false")

# -----------------------------------------------------------------------------
# Base paths
# -----------------------------------------------------------------------------
BASE_DIR = Path(__file__).parent.resolve()

# -----------------------------------------------------------------------------
# Data paths
# -----------------------------------------------------------------------------
DATA_DIR = BASE_DIR / "data"
PROFILE_DATA = DATA_DIR / "profile.json"
SKILLS_DATA = DATA_DIR / "skills.json"
EXPERIENCE_DATA = DATA_DIR / "experience.json"
PROJECTS_DATA = DATA_DIR / "projects.json"
EDUCATION_DATA = DATA_DIR / "education.json"
PROFILE_CONTEXT_DATA = DATA_DIR / "profile_context.json"
DOCS_DIR = DATA_DIR / "docs"

# -----------------------------------------------------------------------------
# Vector database (Chroma)
# -----------------------------------------------------------------------------
CHROMA_DB_DIR = os.path.expanduser("~/.sarjak_portfolio/chroma_db")
COLLECTION_NAME = "sarjak_portfolio"

# -----------------------------------------------------------------------------
# LLM provider settings
# Options: "openai" or "groq"
# -----------------------------------------------------------------------------
LLM_PROVIDER = os.getenv("LLM_PROVIDER", "groq")  # switch provider here
# LLM_PROVIDER = os.getenv("LLM_PROVIDER", "openai")

# -----------------------------------------------------------------------------
# OpenAI API (fallback)
# -----------------------------------------------------------------------------
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
OPENAI_TEMPERATURE = float(os.getenv("OPENAI_TEMPERATURE", "0.3"))

# -----------------------------------------------------------------------------
# Groq Cloud API
# -----------------------------------------------------------------------------
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_MODEL = os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile")
GROQ_TEMPERATURE = float(os.getenv("GROQ_TEMPERATURE", "0.3"))

# -----------------------------------------------------------------------------
# Embeddings
# -----------------------------------------------------------------------------
EMBEDDING_MODEL = os.getenv(
    "EMBEDDING_MODEL", "sentence-transformers/all-MiniLM-L6-v2")

# -----------------------------------------------------------------------------
# RAG settings
# -----------------------------------------------------------------------------
RAG_TOP_K = int(os.getenv("RAG_TOP_K", "8"))
RAG_SCORE_THRESHOLD = float(os.getenv("RAG_SCORE_THRESHOLD", "0.35"))
CHUNK_SIZE = int(os.getenv("CHUNK_SIZE", "850"))
CHUNK_OVERLAP = int(os.getenv("CHUNK_OVERLAP", "150"))

# -----------------------------------------------------------------------------
# Guardrails (privacy/safety)
# -----------------------------------------------------------------------------
SENSITIVE_REGEX = {
    # Matches 123-45-6789 or 9 digits in a row (very permissive—used as a hint, not disclosure)
    "ssn": r"\b\d{3}-\d{2}-\d{4}\b|\b\d{9}\b",
}
SENSITIVE_KEYWORDS = [
    "ssn", "social security", "passport", "bank account", "routing number",
    "credit card", "cvv", "pin", "otp", "one-time password",
    "home address", "exact address", "security code", "password"
]
REFUSAL_MESSAGE = (
    "Sorry, I can’t share that. Please contact Sarjak by email for sensitive information."
)
SAFE_CONTACT_LINE = REFUSAL_MESSAGE  # kept for backward-compatibility

# -----------------------------------------------------------------------------
# UI settings
# -----------------------------------------------------------------------------
APP_TITLE = "Sarjak Maniar - AI/ML Portfolio"
APP_DESCRIPTION = "Chat with me about my experience, projects, and skills!"
SIDEBAR_VISIBLE = True

# Available commands (sidebar + slash commands)
COMMANDS = {
    "/projects":   {"icon": "🚀", "description": "View my projects",          "action": "show_projects"},
    "/experience": {"icon": "💼", "description": "View my work experience",   "action": "show_experience"},
    "/skills":     {"icon": "🎯", "description": "View my technical skills",  "action": "show_skills"},
    "/education":  {"icon": "🎓", "description": "View my education",         "action": "show_education"},
    "/contact":    {"icon": "📧", "description": "Get my contact information", "action": "show_contact"},
}

# -----------------------------------------------------------------------------
# Voice (future)
# -----------------------------------------------------------------------------
VOICE_ENABLED = True
WHISPER_MODEL = os.getenv("WHISPER_MODEL", "base")

# -----------------------------------------------------------------------------
# Logging
# -----------------------------------------------------------------------------
LOG_FILE = BASE_DIR / "logs" / "app.log"
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
