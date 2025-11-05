"""
Slash command handler for instant responses without LLM.
Provides quick access to skills, projects, education, contact info, etc.
"""

from typing import Optional, Tuple
from pathlib import Path
from loguru import logger

from app.config import settings


class CommandHandler:
    """Handles slash commands for instant responses."""

    COMMANDS = {
        "/skills": "Display technical skills and expertise",
        "/projects": "Show all projects with links",
        "/education": "Show education background and research",
        "/contact": "Get contact information",
        "/resume": "Get resume download link",
        "/about": "Quick introduction",
        "/help": "Show available commands"
    }

    @staticmethod
    def is_command(text: str) -> bool:
        """
        Check if text is a slash command.

        Args:
            text: User input text

        Returns:
            True if text starts with a valid command
        """
        text = text.strip().lower()
        return any(text.startswith(cmd) for cmd in CommandHandler.COMMANDS.keys())

    @staticmethod
    def handle_command(text: str) -> Tuple[bool, Optional[str]]:
        """
        Handle a slash command and return the response.

        Args:
            text: User input text (should be a command)

        Returns:
            Tuple of (is_command, response)
            - is_command: True if valid command was processed
            - response: Command output or None if not a command
        """
        text = text.strip().lower()

        if not CommandHandler.is_command(text):
            return (False, None)

        logger.info(f"Processing command: {text}")

        # /help command
        if text.startswith("/help"):
            response = CommandHandler._handle_help()
            return (True, response)

        # /skills command
        if text.startswith("/skills"):
            response = CommandHandler._handle_skills()
            return (True, response)

        # /projects command
        if text.startswith("/projects"):
            response = CommandHandler._handle_projects()
            return (True, response)

        # /education command
        if text.startswith("/education"):
            response = CommandHandler._handle_education()
            return (True, response)

        # /contact command
        if text.startswith("/contact"):
            response = CommandHandler._handle_contact()
            return (True, response)

        # /resume command
        if text.startswith("/resume"):
            response = CommandHandler._handle_resume()
            return (True, response)

        # /about command
        if text.startswith("/about"):
            response = CommandHandler._handle_about()
            return (True, response)

        # Unknown command
        return (True, "Unknown command. Type /help to see available commands.")

    @staticmethod
    def _handle_help() -> str:
        """Return help text with all available commands."""
        help_text = "**Available Commands:**\n\n"
        for cmd, description in CommandHandler.COMMANDS.items():
            help_text += f"• **{cmd}** - {description}\n"
        help_text += "\n💡 You can also ask me questions in natural language about Sarjak's experience, skills, or projects!"
        return help_text

    @staticmethod
    def _handle_skills() -> str:
        """Return formatted skills information."""
        return """**Technical Skills:**

**Programming & Databases:**
- Python (Expert) - 4+ years
- R, SQL (MySQL, PostgreSQL, MongoDB)

**Machine Learning & AI:**
- Scikit-learn, TensorFlow, PyTorch, HuggingFace
- LangChain, LangGraph, LangSmith (Expert)
- RAG, Prompt Engineering, Vector DBs

**Generative AI (Strongest Area):**
- Built 10+ production AI agents
- Expert in LangChain ecosystem
- RAG systems with Pinecone, Chroma, FAISS, Qdrant
- Prompt engineering & LLM optimization

**MLOps & Deployment:**
- Docker, Kubernetes, GitHub Actions
- MLflow, FastAPI, Flask
- AWS (EC2, S3, Lambda), Azure

**Data Science:**
- NumPy, Pandas, Statistical Analysis
- Time-series forecasting, Clustering
- A/B testing, Cohort analysis

💡 Want details on a specific skill? Just ask!
📄 Type **/resume** to download my full resume
🚀 Type **/projects** to see my work"""

    @staticmethod
    def _handle_projects() -> str:
        """Return formatted projects list."""
        return """**Featured Projects:**

**1. LangFlow-Viz** - Workflow graph visualizer for LangGraph
🔗 [GitHub](https://github.com/Sarjak369/langflow-viz) | Published on PyPI
Visualizes AI agent workflows with Graphviz & Mermaid.js

**2. LogSenseAI** - Intelligent log classification framework
🔗 [GitHub](https://github.com/Sarjak369/logsense-ai)
Hybrid system combining ML, transformers & LLMs for log analysis

**3. AI Shop Assistant** - E-commerce chatbot with RAG
🔗 [GitHub](https://github.com/Sarjak369/ai-shop-assistant)
GPT-4o + Pinecone for semantic product search

**4. LinkedIn Post Generator** - AI-powered content creation
🔗 [GitHub](https://github.com/Sarjak369/linkedin-post-generator)
Llama 3.3 via Groq Cloud for style-matching posts

**5. CreditPredictor** - Credit risk classification (85% accuracy)
🔗 [GitHub](https://github.com/Sarjak369/credit-risk-predictor)
XGBoost model deployed on AWS EC2

**+ 7 more projects!**

💡 Ask me: "Tell me more about [project name]"
📱 All projects available on GitHub: [github.com/Sarjak369](https://github.com/Sarjak369)"""

    @staticmethod
    def _handle_education() -> str:
        """Return formatted education information."""
        return """**Education & Research:**

🎓 **Master of Science in Information Technology & Analytics**
Rutgers University | GPA: 3.7/4.0 | 2022-2024

📚 **Relevant Coursework:**
- Algorithmic Machine Learning
- Data Analysis and Visualization
- Business Forecasting
- Multivariate Analysis

🎓 **Bachelor of Engineering in Information Technology**
University of Mumbai | GPA: 9.3/10 | 2018-2022
*First Class with Distinction*

📝 **Published Research Papers:**

1. **"To Laugh or Not to Laugh: LSTM-Based Humor Detection"**
   Deep learning approach using LSTM networks for automated humor detection

2. **"Generation and Grading of Arduous MCQs Using NLP and OMR Detection"**
   Automated MCQ generation with NLP + computer vision grading system

💡 Ask me about specific courses or research work!
📄 Type **/resume** for full academic details"""

    @staticmethod
    def _handle_contact() -> str:
        """Return contact information."""
        return """**Get In Touch:**

📧 **Email:** sarjakm369@gmail.com

💼 **LinkedIn:** [linkedin.com/in/Sarjak369](https://linkedin.com/in/Sarjak369)

🐙 **GitHub:** [github.com/Sarjak369](https://github.com/Sarjak369)

📱 **Phone:** +1 (908) 549-2264

📍 **Location:** Boston, Massachusetts, USA

🎯 **Current Status:**
Actively seeking full-time opportunities in AI/ML and Data Science roles

**Interested in:**
- AI Engineer / ML Engineer roles
- Generative AI & LLM applications
- Remote, hybrid, or on-site (Boston area)
- Willing to relocate for the right opportunity

💡 Feel free to reach out for opportunities or collaborations!"""

    @staticmethod
    def _handle_resume() -> str:
        """Return resume download link."""
        return """**📄 Resume Download:**

You can download my full resume here:
🔗 [Download Resume (PDF)](#resume-download)

**What's included:**
- Complete work experience (4+ years)
- 12+ projects with technologies used
- Technical skills across AI/ML/Data Science
- Education & research publications
- Contact information

💡 After reviewing, let's connect!
📧 Email: sarjakm369@gmail.com
💼 LinkedIn: [linkedin.com/in/Sarjak369](https://linkedin.com/in/Sarjak369)"""

    @staticmethod
    def _handle_about() -> str:
        """Return quick about/introduction."""
        return """**About Sarjak Maniar:**

Hi! I'm Sarjak, an AI Data Scientist based in Boston, USA. I specialize in building intelligent systems that transform data into actionable insights and automated solutions.

**Quick Facts:**
- 🎯 **Role:** AI Data Scientist
- 📍 **Location:** Boston, MA
- 🎓 **Education:** MS from Rutgers (3.7 GPA)
- 💼 **Experience:** 4+ years across AI, ML, and Data Science
- 🚀 **Specialty:** Generative AI, RAG systems, Agentic AI

**What I Do:**
- Build AI agents and agentic systems with LangChain/LangGraph
- Design RAG pipelines for knowledge-intensive applications
- Deploy production ML models on cloud platforms
- Bridge traditional data science with modern AI

**Current Focus:**
Actively seeking full-time AI/ML opportunities where I can apply my expertise in generative AI and data science to solve complex problems.

💡 Ask me about my experience, projects, or skills!
📱 Type **/contact** to get in touch
🚀 Type **/projects** to see my work"""


# Global command handler instance (stateless, so just the class)
command_handler = CommandHandler()
