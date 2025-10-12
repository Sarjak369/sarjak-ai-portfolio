"""
Command routing system for portfolio navigation
"""
from typing import Tuple, Optional
from src.utils.logger import logger
import config


class CommandRouter:
    """Route user commands to appropriate handlers"""

    def __init__(self):
        """Initialize command router"""
        self.commands = config.COMMANDS
        logger.info("Command router initialized")

    def is_command(self, message: str) -> bool:
        """
        Check if message is a command

        Args:
            message: User message

        Returns:
            True if message is a command
        """
        message = message.strip().lower()
        return message.startswith('/') and any(
            message.startswith(cmd.lower()) for cmd in self.commands.keys()
        )

    def parse_command(self, message: str) -> Optional[str]:
        """
        Parse command from message

        Args:
            message: User message

        Returns:
            Command name or None
        """
        message = message.strip().lower()

        for command in self.commands.keys():
            if message.startswith(command.lower()):
                logger.info(f"Command detected: {command}")
                return command

        return None

    def get_command_info(self, command: str) -> dict:
        """
        Get command information

        Args:
            command: Command name

        Returns:
            Command info dictionary
        """
        return self.commands.get(command, {})

    def get_all_commands(self) -> list:
        """Get all available commands"""
        return [
            {
                "command": cmd,
                "icon": info["icon"],
                "description": info["description"]
            }
            for cmd, info in self.commands.items()
        ]
