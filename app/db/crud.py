"""
CRUD (Create, Read, Update, Delete) operations for database models.
"""

from __future__ import annotations
from typing import Optional, List
from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import datetime, timezone
import json
from app.db.models import User, Conversation, Analytics, CachedResponse
from loguru import logger


# ==================== USER OPERATIONS ====================

def create_user(
    db: Session,
    first_name: str,
    last_name: str,
    email: str,
    email_category: str,
    credits: int
) -> User:
    """Create a new user and persist it in the database."""
    user = User(
        first_name=first_name.strip(),
        last_name=last_name.strip(),
        email=email.lower().strip(),
        email_category=email_category,
        is_company_email=(email_category == "company"),
        credits_initial=credits,
        credits_remaining=credits,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    logger.info(f"Created user: {user.email} with {credits} credits")
    return user


def get_user_by_email(db: Session, email: str) -> Optional[User]:
    """Retrieve a user by email (case-insensitive)."""
    return db.query(User).filter(User.email == email.lower().strip()).first()


def get_user_by_id(db: Session, user_id: int) -> Optional[User]:
    """Retrieve a user by their unique ID."""
    return db.query(User).filter(User.id == user_id).first()


def update_user_credits(db: Session, user_id: int, credits_remaining: int) -> Optional[User]:
    """Update the remaining credits for a user."""
    user = get_user_by_id(db, user_id)
    if user is None:
        logger.warning(f"No user found with ID {user_id}")
        return None

    user.credits_remaining = credits_remaining
    user.last_active = datetime.now(timezone.utc)
    db.commit()
    db.refresh(user)
    logger.info(f"Updated credits for {user.email}: {credits_remaining}")
    return user


def deduct_credit(db: Session, user_id: int) -> Optional[User]:
    """Deduct one credit from the user's remaining credits."""
    user = get_user_by_id(db, user_id)
    if user is None:
        logger.warning(f"User not found (ID: {user_id})")
        return None

    if user.credits_remaining <= 0:
        logger.warning(f"User {user.email} has no credits left.")
        return user

    user.credits_remaining -= 1
    user.last_active = datetime.now(timezone.utc)
    db.commit()
    db.refresh(user)
    logger.info(
        f"Deducted one credit from {user.email}. Remaining: {user.credits_remaining}")
    return user


# ==================== CONVERSATION OPERATIONS ====================

def create_conversation(
    db: Session,
    user_id: int,
    question: str,
    answer: str,
    used_llm: bool = True,
    credits_charged: int = 0,
    response_time: Optional[float] = None
) -> Conversation:
    """Create a new conversation record."""
    conversation = Conversation(
        user_id=user_id,
        question=question.strip(),
        answer=answer.strip(),
        used_llm=used_llm,
        credits_charged=credits_charged,
        response_time=response_time,
    )
    db.add(conversation)
    db.commit()
    db.refresh(conversation)
    logger.info(f"Stored conversation for user_id={user_id}")
    return conversation


def get_user_conversations(db: Session, user_id: int, limit: int = 50) -> List[Conversation]:
    """Retrieve recent conversation history for a user."""
    return (
        db.query(Conversation)
        .filter(Conversation.user_id == user_id)
        .order_by(Conversation.created_at.desc())
        .limit(limit)
        .all()
    )


def get_conversation_count(db: Session, user_id: int) -> int:
    """Count total conversations for a specific user."""
    return db.query(Conversation).filter(Conversation.user_id == user_id).count()


# ==================== ANALYTICS OPERATIONS ====================

def create_analytics_event(
    db: Session,
    user_id: int,
    event_type: str,
    event_data: Optional[dict] = None
) -> Analytics:
    """Log an analytics event."""
    analytics = Analytics(
        user_id=user_id,
        event_type=event_type,
        event_data=json.dumps(event_data) if event_data else None
    )
    db.add(analytics)
    db.commit()
    db.refresh(analytics)
    logger.debug(f"Analytics event recorded: {event_type} (user_id={user_id})")
    return analytics


def get_analytics_summary(db: Session) -> dict:
    """Compute and return system-wide analytics summary."""
    total_users = db.query(User).count()
    total_conversations = db.query(Conversation).count()
    total_llm_calls = db.query(Conversation).filter(
        Conversation.used_llm.is_(True)).count()

    cache_hits = total_conversations - total_llm_calls
    cache_hit_rate = (cache_hits / total_conversations *
                      100) if total_conversations else 0.0

    # Email breakdown
    email_breakdown = {
        "personal": db.query(User).filter(User.email_category == "personal").count(),
        "educational": db.query(User).filter(User.email_category == "educational").count(),
        "company": db.query(User).filter(User.email_category == "company").count(),
    }

    return {
        "total_users": total_users,
        "total_conversations": total_conversations,
        "total_llm_calls": total_llm_calls,
        "cache_hit_rate": round(cache_hit_rate, 2),
        "email_breakdown": email_breakdown,
    }


# ==================== CACHE OPERATIONS ====================

def create_cached_response(
    db: Session,
    question: str,
    answer: str,
    embedding: Optional[str] = None
) -> CachedResponse:
    """Store a new cached response for reuse."""
    cached = CachedResponse(
        question=question.strip(),
        answer=answer.strip(),
        embedding=embedding,
    )
    db.add(cached)
    db.commit()
    db.refresh(cached)
    logger.info(f"Cached response stored (ID: {cached.id})")
    return cached


def get_cached_response_by_question(db: Session, question: str) -> Optional[CachedResponse]:
    """Retrieve cached response by exact question match."""
    return db.query(CachedResponse).filter(CachedResponse.question == question.strip()).first()


def increment_cache_hit(db: Session, cache_id: int) -> None:
    """Increment the cache hit counter for a response."""
    cached = db.query(CachedResponse).filter(
        CachedResponse.id == cache_id).first()
    if cached:
        cached.hit_count += 1
        cached.last_used = datetime.now(timezone.utc)
        db.commit()
        logger.debug(f"Incremented cache hit for ID {cache_id}")


def get_all_cached_responses(db: Session) -> List[CachedResponse]:
    """Retrieve all cached responses."""
    return db.query(CachedResponse).all()


def get_popular_questions(db: Session, limit: int = 10) -> List[tuple[str, int]]:
    """Return the most popular questions based on usage frequency."""
    popular = (
        db.query(Conversation.question, func.count(
            Conversation.question).label("count"))
        .group_by(Conversation.question)
        .order_by(func.count(Conversation.question).desc())
        .limit(limit)
        .all()
    )
    return [(q, c) for q, c in popular]
