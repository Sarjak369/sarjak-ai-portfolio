"""
Multi-provider LLM interface - OpenAI or Ollama
"""
from typing import Optional, cast
from langchain_openai import ChatOpenAI
from langchain_ollama import OllamaLLM
from langchain.prompts import PromptTemplate
from src.utils.logger import logger
import config


class LLMInterface:
    """Multi-provider LLM interface supporting OpenAI and Ollama"""

    def __init__(self, provider: Optional[str] = None):
        """
        Initialize LLM interface with specified provider

        Args:
            provider: "openai" or "ollama". If None, uses config setting
        """
        self.provider = provider or config.LLM_PROVIDER
        self.model_name = ""
        self.llm = None

        if self.provider == "openai":
            self._init_openai()
        elif self.provider == "ollama":
            self._init_ollama()
        else:
            raise ValueError(f"Unknown LLM provider: {self.provider}")

    def _init_openai(self):
        """Initialize OpenAI LLM"""
        api_key: str = config.OPENAI_API_KEY or ""  # Default to empty string

        if not api_key:
            raise ValueError(
                "OPENAI_API_KEY not found in environment variables")

        self.llm = ChatOpenAI(
            model=config.OPENAI_MODEL,
            temperature=config.OPENAI_TEMPERATURE,
            # Now it's definitely a str, not None # pyright: ignore[reportArgumentType]
            api_key=api_key  # type: ignore[arg-type]
        )
        self.model_name = config.OPENAI_MODEL
        logger.info(f"✅ OpenAI LLM initialized: {self.model_name}")

    def _init_ollama(self):
        """Initialize Ollama LLM"""
        self.llm = OllamaLLM(
            model=config.OLLAMA_MODEL,
            temperature=config.OLLAMA_TEMPERATURE
        )
        self.model_name = config.OLLAMA_MODEL
        logger.info(f"✅ Ollama LLM initialized: {self.model_name}")

    def generate(self, prompt: str) -> str:
        """
        Generate response from LLM

        Args:
            prompt: User prompt

        Returns:
            Generated text
        """
        try:
            if self.provider == "openai":
                response = self.llm.invoke(prompt)  # type: ignore
                return response.content  # type: ignore
            else:  # ollama
                response = self.llm.invoke(prompt)  # type: ignore
                return str(response)
        except Exception as e:
            logger.error(f"LLM generation failed: {e}")
            return f"Error generating response: {str(e)}"

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

                        Refusal & privacy rules (must follow):
                        - Never provide SSN, passport, bank/financial numbers, exact home address, passwords, PINs, CVVs, OTPs, or similar sensitive data.
                        - If asked for such information, reply: \"{safe_contact}\".
                        - Do not guess. Do not fabricate employers, dates, GPAs, or metrics.

                        Style:
                        - Friendly, concise (2–4 sentences), and professional.
                        - Prefer specific details from context (companies, technologies, metrics).

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

            # Handle different response types
            if self.provider == "openai":
                return response.content  # type: ignore
            else:
                return str(response)
        except Exception as e:
            logger.error(f"Chain execution failed: {e}")
            return f"Error: {str(e)}"

    def get_provider_info(self) -> dict:
        """Get information about current provider"""
        return {
            "provider": self.provider,
            "model": self.model_name,
            "status": "active"
        }
