"""
Prompt Templates for no_more_typo enhanced functionality

Core prompt templates are hardcoded and cannot be overridden by users.
Only the default template (for text without commands) can be customized via environment variables.
"""

import os
from typing import Dict


# Core prompt templates - HARDCODED, cannot be overridden
CORE_TEMPLATES: Dict[str, str] = {
    'translate': """Translate the following text {command_detail}:

{text}

Translation:""",
    
    'elaborate': """Elaborate and expand on the following text with more detail ({command_detail}):

{text}

Elaborated version:""",
    
    'explain': """Explain the following text in clear, simple terms ({command_detail}):

{text}

Explanation:""",
    
    'fix': """Fix any errors or issues in the following ({command_detail}):

{text}

Fixed version:""",
    
    'complete': """Complete the following incomplete content ({command_detail}):

{text}

Completed version:""",
    
    'summarize': """Summarize the following text concisely ({command_detail}):

{text}

Summary:""",
    
    # Generic template for any other command not in specific categories
    'generic': """Process the following text according to this instruction: {command_detail}

{text}

Result:""",
    
    # Default template - can be customized via environment variable
    'default': "Fix the syntax and typos text:\n\n{text}\n\nThe correct string is:"
}


# Command categorization mapping - HARDCODED
COMMAND_CATEGORIES: Dict[str, str] = {
    'translate': 'translate',
    'elaborate': 'elaborate',
    'explain': 'explain',
    'fix': 'fix',
    'complete': 'complete',
    'summarize': 'summarize'
}


def categorize_command(command: str) -> str:
    """
    Categorize a command to determine which template to use.
    
    Args:
        command: The command string (e.g., "translate to spanish")
        
    Returns:
        Template type to use ('translate', 'explain', 'generic', etc.)
    """
    if not command or not isinstance(command, str):
        return 'generic'
    
    # Extract first word as potential category
    words = command.strip().split()
    if not words:  # Handle empty string after strip/split
        return 'generic'
    
    first_word = words[0].lower()
    
    # Return category if known, otherwise use generic
    return COMMAND_CATEGORIES.get(first_word, 'generic')


class PromptManager:
    """Manages prompt templates and builds prompts for LLM processing."""
    
    def __init__(self):
        """Initialize prompt manager with core templates and custom default if provided."""
        # Start with core templates (hardcoded)
        self.templates = CORE_TEMPLATES.copy()
        
        # Allow customization of ONLY the default template via environment variable
        custom_default = os.getenv("NO_MORE_TYPO_PROMPT_TEMPLATE")
        if custom_default:
            # Ensure the custom template includes {text} placeholder
            if "{text}" not in custom_default:
                custom_default += "\n\nCONTEXT:\n{text}"
            self.templates['default'] = custom_default
    
    def get_template(self, template_type: str) -> str:
        """
        Get prompt template by type.
        
        Args:
            template_type: Type of template ('translate', 'explain', 'generic', etc.)
            
        Returns:
            The prompt template string
        """
        if template_type in self.templates:
            return self.templates[template_type]
        
        # Fallback to generic template if type not found
        return self.templates['generic']
    
    def build_prompt(self, template: str, content: str, command: str = "") -> str:
        """
        Build final prompt by substituting variables in template.
        
        Args:
            template: The prompt template string
            content: The cleaned content (text without command)
            command: The command string (optional)
            
        Returns:
            Final prompt ready for LLM
        """
        try:
            return template.format(
                text=content,
                command_detail=command
            )
        except KeyError as e:
            # Handle missing template variables gracefully
            # Fall back to simple substitution
            result = template.replace("{text}", content)
            if command:
                result = result.replace("{command_detail}", command)
            return result
    
    def get_prompt_for_command(self, content: str, command: str) -> str:
        """
        Get complete prompt for a given content and command.
        
        Args:
            content: The cleaned content (text without command)
            command: The command string
            
        Returns:
            Complete prompt ready for LLM
        """
        # Categorize the command
        template_type = categorize_command(command)
        
        # Get appropriate template
        template = self.get_template(template_type)
        
        # Build and return final prompt
        return self.build_prompt(template, content, command)
    
    def get_default_prompt(self, content: str) -> str:
        """
        Get prompt for default processing (no command).
        
        Args:
            content: The content to process
            
        Returns:
            Default prompt ready for LLM
        """
        template = self.get_template('default')
        return self.build_prompt(template, content)
    
    def list_available_templates(self) -> list[str]:
        """
        Get list of available template types.
        
        Returns:
            List of template type names
        """
        return list(self.templates.keys())
    
    def is_core_template(self, template_type: str) -> bool:
        """
        Check if a template type is a core (non-customizable) template.
        
        Args:
            template_type: Template type to check
            
        Returns:
            True if it's a core template, False otherwise
        """
        return template_type in CORE_TEMPLATES and template_type != 'default'


# Convenience functions for backward compatibility and easy use
def get_prompt_manager() -> PromptManager:
    """Get a configured PromptManager instance."""
    return PromptManager()


def build_prompt_for_command(content: str, command: str) -> str:
    """
    Convenience function to build prompt for a command.
    
    Args:
        content: The cleaned content
        command: The command string
        
    Returns:
        Complete prompt ready for LLM
    """
    manager = PromptManager()
    return manager.get_prompt_for_command(content, command)


def build_default_prompt(content: str) -> str:
    """
    Convenience function to build default prompt.
    
    Args:
        content: The content to process
        
    Returns:
        Default prompt ready for LLM
    """
    manager = PromptManager()
    return manager.get_default_prompt(content)


def get_command_category(command: str) -> str:
    """
    Convenience function to get command category.
    
    Args:
        command: The command string
        
    Returns:
        Template category
    """
    return categorize_command(command)