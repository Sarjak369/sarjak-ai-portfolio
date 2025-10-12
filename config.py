"""
Configuration settings for the portfolio application
"""
import os
from pathlib import Path

# Base directory
BASE_DIR = Path(__file__).parent

# Data paths
DATA_DIR = BASE_DIR / "data"
PROFILE_DATA = DATA_DIR / "profile.json"
SKILLS_DATA = DATA_DIR / "skills.json"
EXPERIENCE_DATA = DATA_DIR / "experience.json"
PROJECTS_DATA = DATA_DIR / "projects.json"
EDUCATION_DATA = DATA_DIR / "education.json"

# Vector database
CHROMA_DB_DIR = BASE_DIR / "chroma_db"
COLLECTION_NAME = "sarjak_portfolio"

# LLM settings
LLM_MODEL = "llama3.2"  # Ollama model name
LLM_TEMPERATURE = 0.7
LLM_MAX_TOKENS = 512

# Embedding settings
EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"

# RAG settings
RAG_TOP_K = 3  # Number of documents to retrieve
RAG_SCORE_THRESHOLD = 0.5  # Minimum similarity score

# UI settings
APP_TITLE = "Sarjak Maniar - AI/ML Portfolio"
APP_DESCRIPTION = "Chat with me about my experience, projects, and skills!"
SIDEBAR_VISIBLE = True

# Available commands
COMMANDS = {
    "/projects": {
        "icon": "🚀",
        "description": "View my projects",
        "action": "show_projects"
    },
    "/experience": {
        "icon": "💼",
        "description": "View my work experience",
        "action": "show_experience"
    },
    "/skills": {
        "icon": "🎯",
        "description": "View my technical skills",
        "action": "show_skills"
    },
    "/education": {
        "icon": "🎓",
        "description": "View my education",
        "action": "show_education"
    },
    "/research": {
        "icon": "📚",
        "description": "View my research & publications",
        "action": "show_research"
    },
    "/contact": {
        "icon": "📧",
        "description": "Get my contact information",
        "action": "show_contact"
    }
}

# Voice settings (for future implementation)
VOICE_ENABLED = True
WHISPER_MODEL = "base"  # Options: tiny, base, small, medium, large

# Logging
LOG_FILE = BASE_DIR / "logs" / "app.log"
LOG_LEVEL = "INFO"
