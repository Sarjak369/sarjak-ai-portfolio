"""
LLM integration with Groq for fast inference.
Handles prompt generation, conversation memory, and streaming responses.
"""

from typing import List, Dict, Optional, Any, cast
from groq import Groq
from loguru import logger
from groq.types.chat import ChatCompletionMessageParam
from app.config import settings


class LLMHandler:
    """Handler for LLM operations using Groq."""

    def __init__(self):
        """Initialize the LLM handler."""
        self.client: Optional[Groq] = None
        self.model = settings.LLM_MODEL
        self._initialized = False

    def initialize(self):
        """Initialize the Groq client."""
        try:
            logger.info(f"Initializing Groq LLM with model: {self.model}")

            if not settings.GROQ_API_KEY:
                raise ValueError("GROQ_API_KEY not found in environment")

            self.client = Groq(
                api_key=settings.GROQ_API_KEY.get_secret_value())
            self._initialized = True

            logger.info("LLM initialized successfully")

        except Exception as e:
            logger.error(f"Failed to initialize LLM: {e}")
            raise

    def generate_response(
        self,
        query: str,
        context: str,
        conversation_history: Optional[List[Dict[str, str]]] = None
    ) -> str:
        """
        Generate a response using the Groq LLM.

        Args:
            query: User's question
            context: Retrieved context from RAG
            conversation_history: Previous conversation messages

        Returns:
            Generated response as a string.
        """
        if not self._initialized or not self.client:
            raise RuntimeError("LLM not initialized")

        try:
            logger.info(f"Generating response for query: {query[:50]}...")

            # === System Prompt ===
            system_prompt = """
            You are Sarjak Maniar's AI portfolio assistant. Provide accurate, professional information about Sarjak's background, skills, projects, and experience.

            RESPONSE GUIDELINES:
            - Be direct, concise, and natural
            - Use first person ("I" or "my") when speaking as Sarjak
            - Avoid filler phrases like "I'm excited to share"
            - Get straight to the point
            - Use context to provide specific, accurate details
            - If asked about personal topics (hobbies, personal life) not in context, politely redirect to professional topics
            - Keep responses under 150 words unless more detail is requested
            - Use bullet points for lists
            - Never fabricate information not in the context

            CONTEXT USAGE:
            - Use provided context to answer accurately
            - If context doesn't contain the answer, say "I haven't included that information in my portfolio, but I'm happy to discuss my professional background, projects, and skills"
            - Never make up projects, experiences, or skills
            """

            # --- Build messages as plain dicts ---
            messages: List[Dict[str, Any]] = [
                {"role": "system", "content": system_prompt}
            ]

            # Add up to 6 most recent exchanges from conversation history
            if conversation_history:
                for msg in conversation_history[-6:]:
                    # accept only well-formed items
                    if isinstance(msg, dict) and "role" in msg and "content" in msg:
                        messages.append({
                            "role": str(msg["role"]),
                            "content": str(msg["content"]),
                        })

            # Add user query + context
            user_message = f"""
                Context about Sarjak: {context}

                User question: {query}

                Provide a direct, natural response using the context. Speak as Sarjak in first-person. 
                If the question is about personal topics not in the context (like hobbies), politely redirect to professional topics.
                """

            messages.append({"role": "user", "content": user_message})

            # --- Single cast to the Groq type for the call ---
            typed_messages = cast(List[ChatCompletionMessageParam], messages)

            # === Generate Response ===
            response = self.client.chat.completions.create(
                model=self.model,
                messages=typed_messages,  # casted
                temperature=0.2,   # Lower for consistency
                max_tokens=500,    # Limit verbosity
                top_p=0.9,
            )

            # Safely extract text (avoid NoneType errors)
            answer = (response.choices[0].message.content or "").strip()

            logger.info(f"Generated response ({len(answer)} chars)")
            return answer

        except Exception as e:
            logger.error(f"Error generating response: {e}")
            raise


# Global instance
llm_handler = LLMHandler()
