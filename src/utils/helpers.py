"""
Helper utility functions
"""
import json
import os
from typing import Dict, List, Any
from src.utils.logger import logger


def load_json(file_path: str) -> Dict[str, Any]:
    """
    Load JSON file

    Args:
        file_path: Path to JSON file

    Returns:
        Dictionary containing JSON data
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        logger.info(f"Successfully loaded {file_path}")
        return data
    except FileNotFoundError:
        logger.error(f"File not found: {file_path}")
        return {}
    except json.JSONDecodeError as e:
        logger.error(f"Error decoding JSON from {file_path}: {e}")
        return {}


def save_json(data: Dict[str, Any], file_path: str) -> bool:
    """
    Save data to JSON file

    Args:
        data: Dictionary to save
        file_path: Path to save JSON file

    Returns:
        True if successful, False otherwise
    """
    try:
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        logger.info(f"Successfully saved to {file_path}")
        return True
    except Exception as e:
        logger.error(f"Error saving to {file_path}: {e}")
        return False


def format_tech_tags(technologies: List[str]) -> str:
    """
    Format technology list as HTML tags

    Args:
        technologies: List of technology names

    Returns:
        HTML string with formatted tags
    """
    tags = [f'<span class="tech-tag">{tech}</span>' for tech in technologies]
    return ' '.join(tags)


def format_highlights(highlights: List[str]) -> str:
    """
    Format highlights as bullet points

    Args:
        highlights: List of highlight strings

    Returns:
        HTML string with formatted highlights
    """
    items = [f'<li>{highlight}</li>' for highlight in highlights]
    return f'<ul>{"".join(items)}</ul>'


def create_section_card(title: str, content: str, icon: str = "") -> str:
    """
    Create a styled section card

    Args:
        title: Card title
        content: Card content (HTML)
        icon: Optional emoji icon

    Returns:
        HTML string for section card
    """
    icon_html = f'<span style="font-size: 24px; margin-right: 8px;">{icon}</span>' if icon else ''

    return f"""
    <div class="section-card">
        <div class="section-title">
            {icon_html}{title}
        </div>
        <div class="section-content">
            {content}
        </div>
    </div>
    """


def truncate_text(text: str, max_length: int = 100) -> str:
    """
    Truncate text to maximum length with ellipsis

    Args:
        text: Text to truncate
        max_length: Maximum length

    Returns:
        Truncated text
    """
    if len(text) <= max_length:
        return text
    return text[:max_length].rsplit(' ', 1)[0] + '...'
