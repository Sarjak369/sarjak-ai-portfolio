"""
Format responses beautifully for the UI
"""
from typing import List, Dict, Any
from src.utils.helpers import load_json
from src.utils.logger import logger
import config


class ResponseFormatter:
    """Format different types of responses for the UI"""

    def __init__(self):
        """Initialize response formatter with data"""
        self.profile = load_json(config.PROFILE_DATA)
        self.skills = load_json(config.SKILLS_DATA)
        self.experience = load_json(config.EXPERIENCE_DATA)
        self.projects = load_json(config.PROJECTS_DATA)
        self.education = load_json(config.EDUCATION_DATA)
        logger.info("Response formatter initialized")

    def format_projects(self) -> str:
        """Format projects as beautiful HTML cards"""
        html = '<h2 style="color: #ececf1; margin-bottom: 20px; font-size: 20px; font-weight: 600;">🚀 Featured Projects</h2>'

        if self.projects and "projects" in self.projects:
            for i, project in enumerate(self.projects["projects"], 1):
                tech_tags = "".join([
                    f'<span style="display: inline-block; background: rgba(255,255,255,0.08); color: #c5c5d2; padding: 4px 10px; border-radius: 8px; font-size: 12px; margin: 4px 4px 4px 0; border: 1px solid rgba(255,255,255,0.1);">{tech}</span>'
                    for tech in project.get("technologies", [])
                ])

                html += f'''
                <div style="background: rgba(255,255,255,0.03); padding: 18px; border-radius: 8px; margin-bottom: 16px; border: 1px solid rgba(255,255,255,0.05);">
                    <h3 style="color: #ececf1; margin-bottom: 6px; font-size: 17px; font-weight: 600;">{i}. {project.get('name', '')}</h3>
                    <p style="color: #8e8ea0; font-size: 13px; margin-bottom: 10px; font-style: italic;">{project.get('tagline', '')}</p>
                    <p style="color: #c5c5d2; line-height: 1.6; margin-bottom: 10px; font-size: 15px;">{project.get('description', '')}</p>
                    <div style="margin-top: 10px;">
                        {tech_tags}
                    </div>
                </div>
                '''

        return html

    def format_experience(self) -> str:
        """Format work experience as beautiful HTML cards"""
        html = '<h2 style="color: #ececf1; margin-bottom: 20px; font-size: 20px; font-weight: 600;">💼 Professional Experience</h2>'

        if self.experience and "positions" in self.experience:
            for position in self.experience["positions"]:
                highlights_html = "".join([
                    f'<li style="margin-bottom: 6px; color: #c5c5d2; line-height: 1.6;">{highlight}</li>'
                    for highlight in position.get("highlights", [])
                ])

                tech_tags = "".join([
                    f'<span style="display: inline-block; background: rgba(255,255,255,0.08); color: #c5c5d2; padding: 4px 10px; border-radius: 8px; font-size: 12px; margin: 4px 4px 4px 0; border: 1px solid rgba(255,255,255,0.1);">{tech}</span>'
                    for tech in position.get("technologies", [])
                ])

                html += f'''
                <div style="background: rgba(255,255,255,0.03); padding: 18px; border-radius: 8px; margin-bottom: 16px; border: 1px solid rgba(255,255,255,0.05);">
                    <h3 style="color: #ececf1; margin-bottom: 4px; font-size: 17px; font-weight: 600;">{position.get('title', '')} @ {position.get('company', '')}</h3>
                    <p style="color: #8e8ea0; font-size: 13px; margin-bottom: 10px;">{position.get('duration', '')} | {position.get('location', '')}</p>
                    <ul style="margin: 10px 0; padding-left: 20px; font-size: 15px;">
                        {highlights_html}
                    </ul>
                    <div style="margin-top: 10px;">
                        {tech_tags}
                    </div>
                </div>
                '''

        return html

    def format_skills(self) -> str:
        """Format skills as beautiful HTML cards"""
        html = '<h2 style="color: #ececf1; margin-bottom: 20px; font-size: 20px; font-weight: 600;">🎯 Technical Skills</h2>'

        if self.skills and "categories" in self.skills:
            for category in self.skills["categories"]:
                skill_tags = "".join([
                    f'<span style="display: inline-block; background: rgba(255,255,255,0.08); color: #c5c5d2; padding: 6px 12px; border-radius: 8px; font-size: 13px; margin: 4px 4px 4px 0; border: 1px solid rgba(255,255,255,0.1);">{skill}</span>'
                    for skill in category.get("skills", [])
                ])

                html += f'''
                <div style="background: rgba(255,255,255,0.03); padding: 18px; border-radius: 8px; margin-bottom: 16px; border: 1px solid rgba(255,255,255,0.05);">
                    <h3 style="color: #ececf1; margin-bottom: 12px; font-size: 17px; font-weight: 600;">{category.get('name', '')}</h3>
                    <div>
                        {skill_tags}
                    </div>
                </div>
                '''

        return html

    def format_education(self) -> str:
        """Format education as beautiful HTML cards"""
        html = '<h2 style="color: #ececf1; margin-bottom: 20px; font-size: 20px; font-weight: 600;">🎓 Education</h2>'

        if self.education and "degrees" in self.education:
            for degree in self.education["degrees"]:
                courses = ", ".join(degree.get("courses", []))

                html += f'''
                <div style="background: rgba(255,255,255,0.03); padding: 18px; border-radius: 8px; margin-bottom: 16px; border: 1px solid rgba(255,255,255,0.05);">
                    <h3 style="color: #ececf1; margin-bottom: 4px; font-size: 17px; font-weight: 600;">{degree.get('degree', '')}</h3>
                    <p style="color: #8e8ea0; font-size: 13px; margin-bottom: 8px;">{degree.get('institution', '')} | {degree.get('location', '')}</p>
                    <p style="color: #c5c5d2; margin-bottom: 4px; font-size: 15px;">📅 {degree.get('duration', '')}</p>
                    <p style="color: #c5c5d2; margin-bottom: 10px; font-size: 15px;">📊 GPA: {degree.get('gpa', '')}</p>
                    <p style="color: #8e8ea0; font-size: 14px;"><strong>Relevant Courses:</strong> {courses}</p>
                </div>
                '''

        return html

    def format_contact(self) -> str:
        """Format contact information"""
        html = f'''
        <h2 style="color: #ececf1; margin-bottom: 20px; font-size: 20px; font-weight: 600;">📧 Contact Information</h2>
        <div style="background: rgba(255,255,255,0.03); padding: 18px; border-radius: 8px; border: 1px solid rgba(255,255,255,0.05);">
            <p style="color: #c5c5d2; margin-bottom: 10px; font-size: 15px;">
                📧 <strong>Email:</strong> <a href="mailto:{self.profile.get('email', '')}" style="color: #19c37d; text-decoration: none;">{self.profile.get('email', '')}</a>
            </p>
            <p style="color: #c5c5d2; margin-bottom: 10px; font-size: 15px;">
                📱 <strong>Phone:</strong> {self.profile.get('phone', '')}
            </p>
            <p style="color: #c5c5d2; margin-bottom: 10px; font-size: 15px;">
                💼 <strong>LinkedIn:</strong> <a href="{self.profile.get('links', {}).get('linkedin', '')}" target="_blank" style="color: #19c37d; text-decoration: none;">linkedin.com/in/Sarjak369</a>
            </p>
            <p style="color: #c5c5d2; margin-bottom: 10px; font-size: 15px;">
                🐙 <strong>GitHub:</strong> <a href="{self.profile.get('links', {}).get('github', '')}" target="_blank" style="color: #19c37d; text-decoration: none;">github.com/Sarjak369</a>
            </p>
            <p style="color: #c5c5d2; font-size: 15px;">
                📍 <strong>Location:</strong> {self.profile.get('location', '')}
            </p>
        </div>
        '''
        return html

    def format_command_response(self, command: str) -> str:
        """
        Format response for a specific command

        Args:
            command: Command name

        Returns:
            Formatted HTML response (no wrapper divs)
        """
        formatters = {
            "/projects": self.format_projects,
            "/experience": self.format_experience,
            "/skills": self.format_skills,
            "/education": self.format_education,
            "/contact": self.format_contact
        }

        formatter = formatters.get(command)
        if formatter:
            return formatter()

        return f"<p>Command {command} not implemented yet.</p>"
