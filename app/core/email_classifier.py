# app/core/email_classifier.py

from typing import Tuple
from app.config import settings


class EmailClassifier:
    """Classify email addresses and assign credits."""

    PERSONAL_DOMAINS = [
        'gmail.com', 'yahoo.com', 'outlook.com', 'hotmail.com',
        'icloud.com', 'protonmail.com', 'aol.com', 'mail.com',
        'zoho.com', 'yandex.com', 'live.com', 'msn.com'
    ]

    EDU_PATTERNS = ['.edu', '.ac.uk', '.edu.au', '.edu.in', '.ac.in']

    @staticmethod
    def classify(email: str) -> Tuple[str, int]:
        """
        Classify email and return (category, credits).

        Args:
            email: Email address to classify

        Returns:
            Tuple of (category: str, credits: int)
            Categories: 'personal', 'educational', 'company'
        """
        domain = email.split('@')[1].lower()

        # Check personal domains
        if domain in EmailClassifier.PERSONAL_DOMAINS:
            return ('personal', settings.DEFAULT_CREDITS)

        # Check educational patterns
        if any(domain.endswith(pattern) for pattern in EmailClassifier.EDU_PATTERNS):
            return ('educational', settings.EDU_CREDITS)

        # Default to company email
        return ('company', settings.COMPANY_CREDITS)

    @staticmethod
    def get_welcome_message(category: str, credits: int) -> str:
        """Get personalized welcome message based on email category."""
        messages = {
            'personal': f"✓ Welcome! You have {credits} questions to explore my experience.",
            'educational': f"🎓 Welcome, fellow learner! You have {credits} questions to explore my work.",
            'company': f"✨ Thanks for checking out my profile! You have {credits} questions as a professional."
        }
        return messages.get(category, f"Welcome! You have {credits} questions.")
