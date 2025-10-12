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

    def __init__(self, llm_provider: Optional[str] = None):
        """
        Initialize conversation manager

        Args:
            llm_provider: LLM provider to use (openai or ollama)
        """
        self.router = CommandRouter()
        self.formatter = ResponseFormatter()
        self.rag = RAGRetriever(reset_db=False, llm_provider=llm_provider)

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

        # Check if it's a command
        if self.router.is_command(message):
            command = self.router.parse_command(message)
            if command:
                logger.info(f"Processing command: {command}")
                # Return raw HTML from formatter (no extra wrapper)
                return self.formatter.format_command_response(command)

        # Otherwise, use RAG to answer
        logger.info(f"Processing query with RAG: {message}")
        answer = self.rag.answer_query(message)

        # Return clean answer without extra wrapper divs
        # The app.py will handle the message formatting
        return answer

    def get_stats(self) -> dict:
        """Get system statistics"""
        return self.rag.get_stats()
