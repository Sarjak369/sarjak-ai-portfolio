"""
Load and prepare data for RAG system
"""
import json
from typing import List, Dict, Any
from pathlib import Path
from src.utils.helpers import load_json
from src.utils.logger import logger
import config


class DataLoader:
    """Load and structure portfolio data for RAG"""

    def __init__(self):
        """Initialize data loader"""
        self.profile = load_json(config.PROFILE_DATA)
        self.skills = load_json(config.SKILLS_DATA)
        self.experience = load_json(config.EXPERIENCE_DATA)
        self.projects = load_json(config.PROJECTS_DATA)
        self.education = load_json(config.EDUCATION_DATA)

        logger.info("Data loader initialized")

    def get_all_documents(self) -> List[Dict[str, Any]]:
        """
        Convert all data into documents for RAG

        Returns:
            List of documents with content and metadata
        """
        documents = []

        # Profile document
        if self.profile:
            profile_text = f"""
            Name: {self.profile.get('name', '')}
            Title: {self.profile.get('title', '')}
            Bio: {self.profile.get('bio', '')}
            Location: {self.profile.get('location', '')}
            Email: {self.profile.get('email', '')}
            Phone: {self.profile.get('phone', '')}
            """
            documents.append({
                "content": profile_text,
                "metadata": {
                    "source": "profile",
                    "type": "personal_info"
                }
            })

        # Skills documents
        if self.skills and "categories" in self.skills:
            for category in self.skills["categories"]:
                skills_text = f"""
                Skill Category: {category.get('name', '')}
                Skills: {', '.join(category.get('skills', []))}
                """
                documents.append({
                    "content": skills_text,
                    "metadata": {
                        "source": "skills",
                        "category": category.get('name', ''),
                        "type": "technical_skills"
                    }
                })

        # Experience documents
        if self.experience and "positions" in self.experience:
            for position in self.experience["positions"]:
                highlights = '\n• '.join(position.get('highlights', []))
                exp_text = f"""
                Position: {position.get('title', '')} at {position.get('company', '')}
                Duration: {position.get('duration', '')}
                Location: {position.get('location', '')}
                
                Key Achievements:
                • {highlights}
                
                Technologies: {', '.join(position.get('technologies', []))}
                """
                documents.append({
                    "content": exp_text,
                    "metadata": {
                        "source": "experience",
                        "company": position.get('company', ''),
                        "title": position.get('title', ''),
                        "type": "work_experience"
                    }
                })

        # Project documents
        if self.projects and "projects" in self.projects:
            for project in self.projects["projects"]:
                highlights = '\n• '.join(project.get('highlights', []))
                proj_text = f"""
                Project: {project.get('name', '')}
                Tagline: {project.get('tagline', '')}
                
                Description: {project.get('description', '')}
                
                Key Features:
                • {highlights}
                
                Technologies: {', '.join(project.get('technologies', []))}
                """
                documents.append({
                    "content": proj_text,
                    "metadata": {
                        "source": "projects",
                        "project_name": project.get('name', ''),
                        "type": "project"
                    }
                })

        # Education documents
        if self.education and "degrees" in self.education:
            for degree in self.education["degrees"]:
                courses = ', '.join(degree.get('courses', []))
                edu_text = f"""
                Degree: {degree.get('degree', '')}
                Institution: {degree.get('institution', '')}
                Duration: {degree.get('duration', '')}
                GPA: {degree.get('gpa', '')}
                Relevant Courses: {courses}
                """
                documents.append({
                    "content": edu_text,
                    "metadata": {
                        "source": "education",
                        "institution": degree.get('institution', ''),
                        "type": "education"
                    }
                })

        logger.info(f"Generated {len(documents)} documents for RAG")
        return documents

    def get_summary(self) -> str:
        """
        Get a comprehensive summary of the portfolio

        Returns:
            Summary text
        """
        summary = f"""
        Portfolio Summary for {self.profile.get('name', 'Sarjak Maniar')}
        
        Professional Title: {self.profile.get('title', 'AI/ML Engineer')}
        
        Experience: {len(self.experience.get('positions', []))} positions
        Projects: {len(self.projects.get('projects', []))} major projects
        Education: {len(self.education.get('degrees', []))} degrees
        
        Key Skills: LangChain, LangGraph, RAG, Python, Machine Learning, MLOps
        
        Location: {self.profile.get('location', 'Boston, MA')}
        """
        return summary
