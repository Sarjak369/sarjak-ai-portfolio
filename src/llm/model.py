"""
Multi-provider LLM interface - OpenAI or Groq Cloud
"""
from typing import Optional, cast
from langchain_openai import ChatOpenAI
from langchain_groq import ChatGroq
from langchain_ollama.llms import OllamaLLM
from langchain.prompts import PromptTemplate
from src.utils.logger import logger
import config


class LLMInterface:
    """Multi-provider LLM interface supporting OpenAI or Groq Cloud"""

    def __init__(self, provider: Optional[str] = None):
        """
        Initialize LLM interface with specified provider

        Args:
            provider: "openai" or "groq". If None, uses config setting
        """
        self.provider = provider or config.LLM_PROVIDER
        self.model_name = ""
        self.llm = None

        if self.provider == "openai":
            self._init_openai()
        elif self.provider == "groq":
            self._init_groq()
        else:
            raise ValueError(f"Unknown LLM provider: {self.provider}")

    # ------------------------------------------------------------------
    # OpenAI setup
    # ------------------------------------------------------------------

    def _init_openai(self):
        api_key: str = config.OPENAI_API_KEY or ""
        if not api_key:
            raise ValueError(
                "OPENAI_API_KEY not found in environment variables")

        self.llm = ChatOpenAI(
            model=config.OPENAI_MODEL,
            temperature=config.OPENAI_TEMPERATURE,
            api_key=api_key  # type: ignore[arg-type]
        )
        self.model_name = config.OPENAI_MODEL
        logger.info(f"✅ OpenAI LLM initialized: {self.model_name}")

    # ------------------------------------------------------------------
    # Groq setup
    # ------------------------------------------------------------------
    def _init_groq(self):
        api_key: str = config.GROQ_API_KEY or ""
        if not api_key:
            raise ValueError("GROQ_API_KEY not found in environment variables")

        self.llm = ChatGroq(
            groq_api_key=api_key,  # type: ignore[arg-type]
            model=config.GROQ_MODEL,
            temperature=config.GROQ_TEMPERATURE,
        )
        self.model_name = config.GROQ_MODEL
        logger.info(f"✅ Groq Cloud LLM initialized: {self.model_name}")

    # ------------------------------------------------------------------
    # Generate
    # ------------------------------------------------------------------

    def generate(self, prompt: str) -> str:
        """Generate response from LLM"""
        try:
            response = self.llm.invoke(prompt)  # type: ignore[arg-type]
            return getattr(response, "content", str(response))
        except Exception as e:
            logger.error(f"LLM generation failed: {e}")
            return f"Error generating response: {str(e)}"

    # ------------------------------------------------------------------
    # Generate with context (RAG)
    # ------------------------------------------------------------------

    def generate_with_context(self, query: str, context: str) -> str:
        """
        Generate response with retrieved context using LangChain

        Args:
            query: User query
            context: Retrieved context from RAG

        Returns:
            Generated response
        """
        # Create prompt template
        template = """
        You are Sarjak Maniar’s AI assistant. Use ONLY the provided context to answer.
        If the context does not contain the answer, say you don’t have that information.

        Refusal & privacy rules:
        - Never share SSN, passport, bank/financial details, addresses, or passwords.
        - If asked for such info, reply: "{safe_contact}".
        - Be concise (2–4 sentences), friendly, and professional.

        Context:
        {context}

        User question: {query}

        Answer:
        """

        prompt = PromptTemplate(
            template=template,
            input_variables=["context", "query"]
        )

        # Create chain
        chain = prompt | self.llm  # type: ignore

        try:
            response = chain.invoke({
                "context": context,
                "query": query,
                "safe_contact": config.SAFE_CONTACT_LINE
            })
            return getattr(response, "content", str(response))
        except Exception as e:
            logger.error(f"Chain execution failed: {e}")
            return f"Error: {str(e)}"

    # ------------------------------------------------------------------
    # Provider info
    # ------------------------------------------------------------------

    def get_provider_info(self) -> dict:
        """Get info about the current provider"""
        return {
            "provider": self.provider,
            "model": self.model_name,
            "status": "active"
        }
