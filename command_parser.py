"""
Command Parser for no_more_typo enhanced functionality

Parses clipboard content to extract commands in the format <#command>
and separates the content from the command for further processing.
"""

import re
from typing import Tuple, Optional


class CommandParser:
    """Parses and extracts commands from clipboard content."""
    
    def __init__(self, command_pattern: str = r'<#([^>]+)>'):
        """
        Initialize the command parser.
        
        Args:
            command_pattern: Regex pattern to match commands (default: <#...>)
        """
        self.command_pattern = command_pattern
        self.command_regex = re.compile(command_pattern, re.IGNORECASE)
    
    def parse_clipboard_content(self, text: str) -> Tuple[str, str, bool]:
        """
        Parse clipboard content to extract command and clean content.
        
        Args:
            text: Original clipboard content
            
        Returns:
            Tuple of (clean_content, command, has_command)
            - clean_content: Text with command removed
            - command: Extracted command (empty string if none)
            - has_command: Boolean indicating if command was found
        """
        if not text or not isinstance(text, str):
            return text or "", "", False
        
        command = self.extract_command(text)
        has_command = command is not None and command.strip() != ""
        
        if has_command:
            clean_content = self.clean_content(text)
            return clean_content, command.strip(), True
        else:
            # Return original text if no valid command found
            return text, "", False
    
    def extract_command(self, text: str) -> Optional[str]:
        """
        Extract command from text using regex pattern.
        
        Args:
            text: Text to search for commands
            
        Returns:
            Last command found in text, or None if no command found
        """
        if not text:
            return None
            
        matches = self.command_regex.findall(text)
        if matches:
            # Filter out empty or whitespace-only commands
            valid_commands = [cmd.strip() for cmd in matches if cmd.strip()]
            if valid_commands:
                # Return the last valid command found
                return valid_commands[-1]
        return None
    
    def clean_content(self, text: str) -> str:
        """
        Remove command from original text.
        
        Args:
            text: Original text containing command
            
        Returns:
            Text with command removed and whitespace cleaned
        """
        if not text:
            return text
            
        # Remove all command occurrences
        cleaned = self.command_regex.sub('', text)
        
        # Clean up extra whitespace
        cleaned = cleaned.strip()
        
        # Remove extra spaces that might be left after command removal
        cleaned = re.sub(r'\s+', ' ', cleaned)
        
        return cleaned
    
    def has_command(self, text: str) -> bool:
        """
        Check if text contains a command.
        
        Args:
            text: Text to check
            
        Returns:
            True if command is found, False otherwise
        """
        return self.extract_command(text) is not None
    
    def get_all_commands(self, text: str) -> list[str]:
        """
        Extract all commands from text.
        
        Args:
            text: Text to search for commands
            
        Returns:
            List of all commands found in text
        """
        if not text:
            return []
            
        matches = self.command_regex.findall(text)
        return [match.strip() for match in matches if match.strip()]
    
    def validate_command(self, command: str, max_length: int = 100) -> bool:
        """
        Validate if a command is acceptable.
        
        Args:
            command: Command to validate
            max_length: Maximum allowed command length
            
        Returns:
            True if command is valid, False otherwise
        """
        if not command or not isinstance(command, str):
            return False
            
        command = command.strip()
        
        # Check length
        if len(command) > max_length:
            return False
            
        # Check for empty command
        if not command:
            return False
            
        # Check for potentially dangerous characters (basic validation)
        dangerous_chars = ['<', '>', '{', '}', '|', '&', ';', '$', '`']
        if any(char in command for char in dangerous_chars):
            return False
            
        return True


# Convenience functions for backward compatibility and ease of use
def parse_command(text: str) -> Tuple[str, str, bool]:
    """
    Convenience function to parse command from text.
    
    Args:
        text: Text to parse
        
    Returns:
        Tuple of (clean_content, command, has_command)
    """
    parser = CommandParser()
    return parser.parse_clipboard_content(text)


def extract_command_simple(text: str) -> Optional[str]:
    """
    Simple function to extract command from text.
    
    Args:
        text: Text to search
        
    Returns:
        Command if found, None otherwise
    """
    parser = CommandParser()
    return parser.extract_command(text)


def clean_text(text: str) -> str:
    """
    Simple function to clean command from text.
    
    Args:
        text: Text to clean
        
    Returns:
        Cleaned text
    """
    parser = CommandParser()
    return parser.clean_content(text)