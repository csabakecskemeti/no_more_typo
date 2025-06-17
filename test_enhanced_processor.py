"""
Integration tests for EnhancedProcessor

Tests the complete integration of command parsing, prompt templates,
and LLM processing without actually calling the LLM (using mocks).
"""

import pytest
from unittest.mock import Mock, patch
from enhanced_processor import (
    EnhancedProcessor, 
    ProcessorFactory,
    process_clipboard_content,
    process_with_command,
    get_preview_prompt
)


class TestEnhancedProcessor:
    """Test suite for EnhancedProcessor integration."""
    
    def setup_method(self):
        """Set up test fixtures with mocked LLM."""
        # Create mock LLM to avoid actual API calls
        self.mock_llm = Mock()
        self.mock_llm.invoke.return_value = "Mocked LLM response"
        
        # Create processor with mocked LLM
        self.processor = EnhancedProcessor(llm=self.mock_llm)
    
    def test_processor_initialization(self):
        """Test that processor initializes correctly."""
        processor = EnhancedProcessor(llm=self.mock_llm)
        
        assert processor.command_parser is not None
        assert processor.prompt_manager is not None
        assert processor.llm is not None
        assert processor.cleanup is not None
    
    def test_process_content_with_command(self):
        """Test processing content with a command."""
        clipboard_text = "Hello world <#translate to spanish>"
        
        # Mock LLM response
        self.mock_llm.invoke.return_value = '"Hola mundo"'
        
        result = self.processor.process_clipboard_content(clipboard_text)
        
        # Should have called LLM with appropriate prompt
        assert self.mock_llm.invoke.called
        call_args = self.mock_llm.invoke.call_args[0][0]
        assert "translate to spanish" in call_args
        assert "Hello world" in call_args
        
        # Should clean up the response (remove quotes)
        assert result == "Hola mundo"
    
    def test_process_content_without_command(self):
        """Test processing content without a command (default behavior)."""
        clipboard_text = "Helo wrold with typos"
        
        # Mock traditional chain response
        with patch.object(self.processor, 'traditional_chain') as mock_chain:
            mock_chain.invoke.return_value = "Hello world with typos"
            
            result = self.processor.process_clipboard_content(clipboard_text)
            
            # Should use traditional chain for default processing
            assert mock_chain.invoke.called
            call_args = mock_chain.invoke.call_args[0][0]
            assert call_args["text"] == clipboard_text
            
            assert result == "Hello world with typos"
    
    def test_process_with_specific_command_categories(self):
        """Test processing with different command categories."""
        test_cases = [
            ("Code with bugs", "fix syntax errors", "fix"),
            ("Short text", "elaborate with details", "elaborate"),
            ("Complex concept", "explain simply", "explain"),
            ("Incomplete function", "complete implementation", "complete"),
            ("Long article", "summarize key points", "summarize"),
            ("Custom request", "make this more formal", "generic")
        ]
        
        for content, command, expected_category in test_cases:
            # Reset mock
            self.mock_llm.reset_mock()
            self.mock_llm.invoke.return_value = f"Processed {content}"
            
            # Process with command
            result = self.processor.process_with_specific_command(content, command)
            
            # Verify LLM was called
            assert self.mock_llm.invoke.called
            
            # Verify command category detection
            category = self.processor.get_command_category(command)
            assert category == expected_category
            
            # Verify result
            assert result == f"Processed {content}"
    
    def test_command_validation(self):
        """Test command validation."""
        valid_commands = [
            "translate to french",
            "explain this concept", 
            "fix errors",
            "complete function"
        ]
        
        invalid_commands = [
            "",  # Empty
            "a" * 150,  # Too long
            "command with <brackets>",  # Dangerous chars
        ]
        
        for cmd in valid_commands:
            assert self.processor.validate_command(cmd) is True
        
        for cmd in invalid_commands:
            assert self.processor.validate_command(cmd) is False
    
    def test_command_support_detection(self):
        """Test detection of supported vs generic commands."""
        supported_commands = [
            "translate to spanish",
            "explain this",
            "fix bugs",
            "elaborate details",
            "complete code",
            "summarize article"
        ]
        
        generic_commands = [
            "make this formal",
            "convert to typescript",
            "optimize performance"
        ]
        
        for cmd in supported_commands:
            assert self.processor.is_command_supported(cmd) is True
        
        for cmd in generic_commands:
            assert self.processor.is_command_supported(cmd) is False
    
    def test_preview_prompt_functionality(self):
        """Test prompt preview functionality."""
        content = "Hello world"
        command = "translate to french"
        
        # Test command prompt preview
        prompt = self.processor.preview_prompt(content, command)
        assert "translate to french" in prompt
        assert "Hello world" in prompt
        assert "Translation:" in prompt
        
        # Test default prompt preview
        default_prompt = self.processor.preview_prompt(content)
        assert "Hello world" in default_prompt
        assert "Fix the syntax and typos" in default_prompt
    
    def test_error_handling_with_command_processing(self):
        """Test error handling when command processing fails."""
        clipboard_text = "Hello world <#translate to spanish>"
        
        # Mock LLM to raise exception
        self.mock_llm.invoke.side_effect = Exception("LLM error")
        
        # Mock traditional chain as fallback
        with patch.object(self.processor, 'traditional_chain') as mock_chain:
            mock_chain.invoke.return_value = "Fallback result"
            
            with patch('warnings.warn') as mock_warn:
                result = self.processor.process_clipboard_content(clipboard_text)
                
                # Should fall back to default processing
                assert mock_chain.invoke.called
                assert result == "Fallback result"
                
                # Should warn about the failure
                assert mock_warn.called
    
    def test_error_handling_with_complete_failure(self):
        """Test error handling when everything fails."""
        clipboard_text = "Hello world <#translate to spanish>"
        
        # Mock both LLM and traditional chain to fail
        self.mock_llm.invoke.side_effect = Exception("LLM error")
        
        with patch.object(self.processor, 'traditional_chain') as mock_chain:
            mock_chain.invoke.side_effect = Exception("Chain error")
            
            with patch('warnings.warn') as mock_warn:
                result = self.processor.process_clipboard_content(clipboard_text)
                
                # Should return original content as ultimate fallback
                assert result == "Hello world"  # Command removed
                
                # Should warn about failures
                assert mock_warn.call_count >= 1
    
    def test_available_commands_listing(self):
        """Test listing of available commands."""
        commands = self.processor.get_available_commands()
        
        expected_commands = [
            'translate', 'elaborate', 'explain', 'fix', 
            'complete', 'summarize', 'generic', 'default'
        ]
        
        for cmd in expected_commands:
            assert cmd in commands
    
    def test_edge_cases_with_empty_input(self):
        """Test edge cases with empty or None input."""
        # Empty string
        result = self.processor.process_clipboard_content("")
        assert result == ""
        
        # None input
        result = self.processor.process_clipboard_content(None)
        assert result == ""
        
        # Whitespace only
        with patch.object(self.processor, 'traditional_chain') as mock_chain:
            mock_chain.invoke.return_value = "   "
            result = self.processor.process_clipboard_content("   ")
            assert mock_chain.invoke.called


class TestProcessorFactory:
    """Test suite for ProcessorFactory."""
    
    def test_create_default_processor(self):
        """Test creating default processor."""
        processor = ProcessorFactory.create_default_processor()
        
        assert isinstance(processor, EnhancedProcessor)
        assert processor.llm is not None
        assert processor.command_parser is not None
        assert processor.prompt_manager is not None
    
    def test_create_processor_with_custom_llm(self):
        """Test creating processor with custom LLM."""
        mock_llm = Mock()
        processor = ProcessorFactory.create_processor_with_llm(mock_llm)
        
        assert isinstance(processor, EnhancedProcessor)
        assert processor.llm is mock_llm
    
    def test_create_processor_for_testing(self):
        """Test creating processor configured for testing."""
        processor = ProcessorFactory.create_processor_for_testing()
        
        assert isinstance(processor, EnhancedProcessor)
        # Should suppress warnings (tested by not raising warnings)


class TestConvenienceFunctions:
    """Test suite for convenience functions."""
    
    @patch('enhanced_processor.EnhancedProcessor')
    def test_process_clipboard_content_function(self, mock_processor_class):
        """Test process_clipboard_content convenience function."""
        mock_processor = Mock()
        mock_processor.process_clipboard_content.return_value = "Processed content"
        mock_processor_class.return_value = mock_processor
        
        result = process_clipboard_content("Test content")
        
        assert mock_processor_class.called
        assert mock_processor.process_clipboard_content.called_with("Test content")
        assert result == "Processed content"
    
    @patch('enhanced_processor.EnhancedProcessor')
    def test_process_with_command_function(self, mock_processor_class):
        """Test process_with_command convenience function."""
        mock_processor = Mock()
        mock_processor.process_with_specific_command.return_value = "Command result"
        mock_processor_class.return_value = mock_processor
        
        result = process_with_command("Content", "command")
        
        assert mock_processor_class.called
        assert mock_processor.process_with_specific_command.called_with("Content", "command")
        assert result == "Command result"
    
    @patch('enhanced_processor.EnhancedProcessor')
    def test_get_preview_prompt_function(self, mock_processor_class):
        """Test get_preview_prompt convenience function."""
        mock_processor = Mock()
        mock_processor.preview_prompt.return_value = "Preview prompt"
        mock_processor_class.return_value = mock_processor
        
        result = get_preview_prompt("Content", "command")
        
        assert mock_processor_class.called
        assert mock_processor.preview_prompt.called_with("Content", "command")
        assert result == "Preview prompt"


class TestRealWorldScenarios:
    """Test suite for real-world usage scenarios."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.mock_llm = Mock()
        self.processor = EnhancedProcessor(llm=self.mock_llm)
    
    def test_code_completion_scenario(self):
        """Test real-world code completion scenario."""
        clipboard_text = "def fibonacci(n): <#complete this function>"
        
        self.mock_llm.invoke.return_value = '''def fibonacci(n):
    if n <= 1:
        return n
    return fibonacci(n-1) + fibonacci(n-2)'''
        
        result = self.processor.process_clipboard_content(clipboard_text)
        
        # Should generate appropriate prompt
        call_args = self.mock_llm.invoke.call_args[0][0]
        assert "Complete the following incomplete content" in call_args
        assert "def fibonacci(n):" in call_args
        
        # Should return completed function
        assert "def fibonacci(n):" in result
        assert "if n <= 1:" in result
    
    def test_translation_scenario(self):
        """Test real-world translation scenario."""
        clipboard_text = "Bonjour le monde <#translate to english>"
        
        self.mock_llm.invoke.return_value = "Hello world"
        
        result = self.processor.process_clipboard_content(clipboard_text)
        
        # Should generate translation prompt
        call_args = self.mock_llm.invoke.call_args[0][0]
        assert "Translate the following text" in call_args
        assert "Bonjour le monde" in call_args
        
        assert result == "Hello world"
    
    def test_explanation_scenario(self):
        """Test real-world explanation scenario."""
        clipboard_text = "Machine learning <#explain in simple terms>"
        
        self.mock_llm.invoke.return_value = "Machine learning is when computers learn patterns from data without being explicitly programmed."
        
        result = self.processor.process_clipboard_content(clipboard_text)
        
        # Should generate explanation prompt
        call_args = self.mock_llm.invoke.call_args[0][0]
        assert "Explain the following text" in call_args
        assert "Machine learning" in call_args
        
        assert "computers learn patterns" in result
    
    def test_generic_command_scenario(self):
        """Test real-world generic command scenario."""
        clipboard_text = "function hello() { } <#convert to typescript>"
        
        self.mock_llm.invoke.return_value = "function hello(): void { }"
        
        result = self.processor.process_clipboard_content(clipboard_text)
        
        # Should generate generic prompt
        call_args = self.mock_llm.invoke.call_args[0][0]
        assert "Process the following text according to this instruction: convert to typescript" in call_args
        assert "function hello() { }" in call_args
        
        assert result == "function hello(): void { }"


if __name__ == "__main__":
    # Run the tests
    pytest.main([__file__, "-v"])