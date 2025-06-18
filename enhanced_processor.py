"""
Enhanced Processor for no_more_typo with command support

Integrates command parsing and prompt template management to provide
enhanced clipboard processing with command-based functionality.
"""

from typing import Optional
from command_parser import CommandParser
from prompt_templates import PromptManager
from langchain_community.llms.openai import OpenAI
from langchain_core.prompts import PromptTemplate
from langchain.schema.runnable import RunnableLambda
import warnings


class EnhancedProcessor:
    """
    Enhanced processor that handles both traditional typo fixing and command-based processing.
    
    This processor integrates:
    - Command parsing to extract <#command> instructions
    - Prompt template management for different command types
    - LLM processing with appropriate prompts
    - Backward compatibility with original typo-fixing functionality
    """
    
    def __init__(self, llm: Optional[OpenAI] = None):
        """
        Initialize the enhanced processor.
        
        Args:
            llm: Optional LLM instance. If not provided, creates a new OpenAI instance.
        """
        # Initialize components
        self.command_parser = CommandParser()
        self.prompt_manager = PromptManager()
        
        # Initialize LLM
        if llm is None:
            self.llm = OpenAI()
        else:
            self.llm = llm
        
        # Create cleanup function
        self.cleanup = RunnableLambda(
            lambda x: x.strip().strip('"').strip("'")
        )
        
        # Create traditional chain for backward compatibility
        self._setup_traditional_chain()
    
    def _setup_traditional_chain(self):
        """Set up the traditional no_typo chain for backward compatibility."""
        # Get default prompt template
        default_template_str = self.prompt_manager.get_template('default')
        
        # Create LangChain PromptTemplate
        default_prompt = PromptTemplate.from_template(default_template_str)
        
        # Create traditional chain
        self.traditional_chain = default_prompt | self.llm | self.cleanup
    
    def process_clipboard_content(self, clipboard_text: str) -> str:
        """
        Main processing method for clipboard content.
        
        Args:
            clipboard_text: Raw clipboard content that may contain commands
            
        Returns:
            Processed content ready to be copied back to clipboard
        """
        if not clipboard_text or not isinstance(clipboard_text, str):
            return clipboard_text or ""
        
        try:
            # Parse clipboard content for commands
            content, command, has_command = self.command_parser.parse_clipboard_content(clipboard_text)
            
            if has_command:
                return self._process_with_command(content, command)
            else:
                return self._process_default(content)
                
        except Exception as e:
            # Fallback to original content if processing fails
            warnings.warn(f"Enhanced processing failed: {e}. Falling back to original content.")
            return clipboard_text
    
    def _process_with_command(self, content: str, command: str) -> str:
        """
        Process content with a specific command.
        
        Args:
            content: Cleaned content (command removed)
            command: The command to execute
            
        Returns:
            Processed content based on the command
        """
        try:
            # Generate prompt for the command
            prompt = self.prompt_manager.get_prompt_for_command(content, command)
            
            # Process with LLM
            result = self.llm.invoke(prompt)
            
            # Clean up result
            return self.cleanup.invoke(result)
            
        except Exception as e:
            # Fallback to default processing if command processing fails
            warnings.warn(f"Command processing failed for '{command}': {e}. Falling back to default processing.")
            return self._process_default(content)
    
    def _process_default(self, content: str) -> str:
        """
        Process content with default typo-fixing behavior.
        
        Args:
            content: Content to process
            
        Returns:
            Processed content with typos fixed
        """
        try:
            # Use traditional chain for backward compatibility
            return self.traditional_chain.invoke({"text": content})
            
        except Exception as e:
            # Ultimate fallback to original content
            warnings.warn(f"Default processing failed: {e}. Returning original content.")
            return content
    
    def process_with_specific_command(self, content: str, command: str) -> str:
        """
        Public method to process content with a specific command.
        
        Args:
            content: Content to process
            command: Command to execute
            
        Returns:
            Processed content
        """
        return self._process_with_command(content, command)
    
    def get_available_commands(self) -> list[str]:
        """
        Get list of available command categories.
        
        Returns:
            List of available command types
        """
        return self.prompt_manager.list_available_templates()
    
    def is_command_supported(self, command: str) -> bool:
        """
        Check if a command is supported (has a specific template).
        
        Args:
            command: Command to check
            
        Returns:
            True if command has specific support, False if it uses generic template
        """
        from prompt_templates import categorize_command
        category = categorize_command(command)
        return category != 'generic'
    
    def preview_prompt(self, content: str, command: str = None) -> str:
        """
        Preview the prompt that would be sent to the LLM.
        
        Args:
            content: Content to process
            command: Optional command (if None, uses default)
            
        Returns:
            The prompt that would be sent to LLM
        """
        if command:
            return self.prompt_manager.get_prompt_for_command(content, command)
        else:
            return self.prompt_manager.get_default_prompt(content)
    
    def validate_command(self, command: str) -> bool:
        """
        Validate if a command is safe and well-formed.
        
        Args:
            command: Command to validate
            
        Returns:
            True if command is valid, False otherwise
        """
        return self.command_parser.validate_command(command)
    
    def get_command_category(self, command: str) -> str:
        """
        Get the category for a command.
        
        Args:
            command: Command to categorize
            
        Returns:
            Category name ('translate', 'explain', 'generic', etc.)
        """
        from prompt_templates import categorize_command
        return categorize_command(command)


class ProcessorFactory:
    """Factory class for creating configured processor instances."""
    
    @staticmethod
    def create_default_processor() -> EnhancedProcessor:
        """
        Create processor with default configuration.
        
        Returns:
            Configured EnhancedProcessor instance
        """
        return EnhancedProcessor()
    
    @staticmethod
    def create_processor_with_llm(llm: OpenAI) -> EnhancedProcessor:
        """
        Create processor with custom LLM instance.
        
        Args:
            llm: Configured LLM instance
            
        Returns:
            Configured EnhancedProcessor instance
        """
        return EnhancedProcessor(llm=llm)
    
    @staticmethod
    def create_processor_for_testing() -> EnhancedProcessor:
        """
        Create processor configured for testing (with warnings suppressed).
        
        Returns:
            Configured EnhancedProcessor instance for testing
        """
        # Suppress warnings for testing
        warnings.filterwarnings("ignore")
        return EnhancedProcessor()


# Convenience functions for backward compatibility
def process_clipboard_content(clipboard_text: str) -> str:
    """
    Convenience function to process clipboard content.
    
    Args:
        clipboard_text: Raw clipboard content
        
    Returns:
        Processed content
    """
    processor = EnhancedProcessor()
    return processor.process_clipboard_content(clipboard_text)


def process_with_command(content: str, command: str) -> str:
    """
    Convenience function to process content with a specific command.
    
    Args:
        content: Content to process
        command: Command to execute
        
    Returns:
        Processed content
    """
    processor = EnhancedProcessor()
    return processor.process_with_specific_command(content, command)


def get_preview_prompt(content: str, command: str = None) -> str:
    """
    Convenience function to preview prompt.
    
    Args:
        content: Content to process
        command: Optional command
        
    Returns:
        Prompt that would be sent to LLM
    """
    processor = EnhancedProcessor()
    return processor.preview_prompt(content, command)