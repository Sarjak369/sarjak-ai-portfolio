"""
Conversation state management
"""
from typing import List, Tuple, Optional
from src.agent.router import CommandRouter
from src.agent.response_formatter import ResponseFormatter
from src.rag.retriever import RAGRetriever
from src.utils.logger import logger


class ConversationManager:
    """Manage conversation flow and state"""

    # 🔹 Cache a shared retriever + model across all instances
    _shared_rag = None

    def __init__(self, llm_provider: Optional[str] = None):
        """
        Initialize conversation manager

        Args:
            llm_provider: LLM provider to use (openai or groq)
        """
        self.router = CommandRouter()
        self.formatter = ResponseFormatter()

        # ⚡ Use global retriever cache to avoid reloading sentence-transformer each time
        if ConversationManager._shared_rag is None:
            logger.info(
                "Loading RAGRetriever and model for the first time (this may take a few seconds)...")
            ConversationManager._shared_rag = RAGRetriever(
                reset_db=False, llm_provider=llm_provider)
            logger.info("✅ RAGRetriever and model cached for reuse")

        self.rag = ConversationManager._shared_rag
        logger.info("Conversation manager initialized")

    def process_message(self, message: str) -> str:
        """
        Process user message and generate response

        Args:
            message: User message

        Returns:
            Response text (HTML formatted)
        """
        if not message or not message.strip():
            return "Please enter a message."

        message = message.strip()

        # If user typed a command like /skills, /projects, etc.
        if self.router.is_command(message):
            command = self.router.parse_command(message)
            if command:
                logger.info(f"Processing command: {command}")
                # Return HTML from formatter (no wrapper divs)
                return self.formatter.format_command_response(command)

        # Otherwise, use RAG for natural questions
        logger.info(f"Processing query with RAG: {message}")
        try:
            answer = self.rag.answer_query(message)
        except Exception as e:
            logger.error(f"RAG query failed: {e}")
            return "⚠️ Something went wrong while processing your query. Please try again."

        return answer

    def get_stats(self) -> dict:
        """Get system statistics"""
        try:
            return self.rag.get_stats()
        except Exception:
            return {"status": "error", "details": "RAG not ready"}
