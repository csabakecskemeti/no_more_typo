"""
Unit tests for PromptManager and prompt template functionality

Tests the template selection, command categorization, and prompt building.
"""

import pytest
import os
from unittest.mock import patch
from prompt_templates import (
    PromptManager, 
    categorize_command, 
    CORE_TEMPLATES, 
    COMMAND_CATEGORIES,
    build_prompt_for_command,
    build_default_prompt,
    get_command_category
)


class TestCommandCategorization:
    """Test suite for command categorization."""
    
    def test_basic_command_categorization(self):
        """Test basic command categorization."""
        test_cases = [
            ("translate", "translate"),
            ("translate to spanish", "translate"),
            ("explain", "explain"),
            ("explain this concept", "explain"),
            ("fix", "fix"),
            ("fix this bug", "fix"),
            ("elaborate", "elaborate"),
            ("elaborate on this topic", "elaborate"),
            ("complete", "complete"),
            ("complete this function", "complete"),
            ("summarize", "summarize"),
            ("summarize this article", "summarize"),
        ]
        
        for command, expected_category in test_cases:
            category = categorize_command(command)
            assert category == expected_category
    
    def test_unknown_commands_use_generic(self):
        """Test that unknown commands use generic category."""
        unknown_commands = [
            "refactor this code",
            "optimize performance", 
            "convert to typescript",
            "make this more formal",
            "rewrite in python"
        ]
        
        for command in unknown_commands:
            category = categorize_command(command)
            assert category == "generic"
    
    def test_case_insensitive_categorization(self):
        """Test that command categorization is case insensitive."""
        test_cases = [
            ("TRANSLATE", "translate"),
            ("Explain", "explain"),
            ("FIX", "fix"),
            ("eLaBoRaTe", "elaborate")
        ]
        
        for command, expected_category in test_cases:
            category = categorize_command(command)
            assert category == expected_category
    
    def test_edge_cases(self):
        """Test edge cases for command categorization."""
        # Empty or None commands
        assert categorize_command("") == "generic"
        assert categorize_command(None) == "generic"
        assert categorize_command("   ") == "generic"
        
        # Non-string input
        assert categorize_command(123) == "generic"
        assert categorize_command([]) == "generic"
    
    def test_commands_with_extra_whitespace(self):
        """Test commands with extra whitespace."""
        assert categorize_command("  translate  to spanish  ") == "translate"
        assert categorize_command("\texplain\tthis\t") == "explain"


class TestPromptManager:
    """Test suite for PromptManager class."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.manager = PromptManager()
    
    def test_initialization_with_core_templates(self):
        """Test that PromptManager initializes with core templates."""
        manager = PromptManager()
        
        # Should have all core template types
        for template_type in CORE_TEMPLATES.keys():
            assert template_type in manager.templates
            assert manager.get_template(template_type) is not None
    
    @patch.dict(os.environ, {'NO_MORE_TYPO_PROMPT_TEMPLATE': 'Custom default: {text}'})
    def test_custom_default_template(self):
        """Test custom default template from environment variable."""
        manager = PromptManager()
        
        # Default template should be customized
        default_template = manager.get_template('default')
        assert "Custom default:" in default_template
        
        # Core templates should remain unchanged
        translate_template = manager.get_template('translate')
        assert translate_template == CORE_TEMPLATES['translate']
    
    @patch.dict(os.environ, {'NO_MORE_TYPO_PROMPT_TEMPLATE': 'Missing placeholder'})
    def test_custom_default_template_missing_placeholder(self):
        """Test custom default template without {text} placeholder."""
        manager = PromptManager()
        
        # Should automatically add {text} placeholder
        default_template = manager.get_template('default')
        assert "{text}" in default_template
        assert "Missing placeholder" in default_template
    
    def test_get_template_fallback(self):
        """Test template fallback for unknown types."""
        unknown_template = self.manager.get_template('unknown_type')
        generic_template = self.manager.get_template('generic')
        
        assert unknown_template == generic_template
    
    def test_build_prompt_basic(self):
        """Test basic prompt building."""
        template = "Process this: {text} with command: {command_detail}"
        content = "Hello world"
        command = "translate to spanish"
        
        prompt = self.manager.build_prompt(template, content, command)
        
        assert "Hello world" in prompt
        assert "translate to spanish" in prompt
        assert "Process this:" in prompt
    
    def test_build_prompt_missing_variables(self):
        """Test prompt building with missing template variables."""
        template = "Process this: {text} with {missing_var}"
        content = "Hello world"
        command = "test command"
        
        # Should handle missing variables gracefully
        prompt = self.manager.build_prompt(template, content, command)
        assert "Hello world" in prompt
        # Should still contain the missing variable placeholder or handle it gracefully
        assert len(prompt) > 0
    
    def test_get_prompt_for_command(self):
        """Test complete prompt generation for commands."""
        content = "Hello world"
        command = "translate to spanish"
        
        prompt = self.manager.get_prompt_for_command(content, command)
        
        assert "Hello world" in prompt
        assert "translate to spanish" in prompt
        assert "Translation:" in prompt  # From translate template
    
    def test_get_default_prompt(self):
        """Test default prompt generation."""
        content = "Helo wrold"
        
        prompt = self.manager.get_default_prompt(content)
        
        assert "Helo wrold" in prompt
        assert "Fix the syntax and typos" in prompt
    
    def test_list_available_templates(self):
        """Test listing available templates."""
        templates = self.manager.list_available_templates()
        
        expected_templates = list(CORE_TEMPLATES.keys())
        assert set(templates) == set(expected_templates)
    
    def test_is_core_template(self):
        """Test core template identification."""
        # Core templates (non-customizable)
        assert self.manager.is_core_template('translate') is True
        assert self.manager.is_core_template('explain') is True
        assert self.manager.is_core_template('fix') is True
        
        # Default template (customizable)
        assert self.manager.is_core_template('default') is False
        
        # Non-existent template
        assert self.manager.is_core_template('unknown') is False


class TestPromptGeneration:
    """Test suite for end-to-end prompt generation."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.manager = PromptManager()
    
    def test_translate_command_prompt(self):
        """Test translate command prompt generation."""
        content = "Bonjour le monde"
        command = "translate to english"
        
        prompt = self.manager.get_prompt_for_command(content, command)
        
        assert "Translate the following text translate to english:" in prompt
        assert "Bonjour le monde" in prompt
        assert "Translation:" in prompt
    
    def test_explain_command_prompt(self):
        """Test explain command prompt generation."""
        content = "Machine learning"
        command = "explain in simple terms"
        
        prompt = self.manager.get_prompt_for_command(content, command)
        
        assert "Explain the following text in clear, simple terms" in prompt
        assert "explain in simple terms" in prompt  # command detail included
        assert "Machine learning" in prompt
        assert "Explanation:" in prompt
    
    def test_fix_command_prompt(self):
        """Test fix command prompt generation."""
        content = "def hello( print('hello')"
        command = "fix syntax errors"
        
        prompt = self.manager.get_prompt_for_command(content, command)
        
        assert "Fix any errors or issues in the following" in prompt
        assert "fix syntax errors" in prompt  # command detail included
        assert "def hello(" in prompt
        assert "Fixed version:" in prompt
    
    def test_generic_command_prompt(self):
        """Test generic command prompt generation."""
        content = "function myFunc() { }"
        command = "convert to typescript"
        
        prompt = self.manager.get_prompt_for_command(content, command)
        
        assert "Process the following text according to this instruction: convert to typescript" in prompt
        assert "function myFunc() { }" in prompt
        assert "Result:" in prompt
    
    def test_elaborate_command_prompt(self):
        """Test elaborate command prompt generation."""
        content = "AI is powerful"
        command = "elaborate with examples"
        
        prompt = self.manager.get_prompt_for_command(content, command)
        
        assert "Elaborate and expand on the following text with more detail" in prompt
        assert "elaborate with examples" in prompt  # command detail included
        assert "AI is powerful" in prompt
        assert "Elaborated version:" in prompt
    
    def test_complete_command_prompt(self):
        """Test complete command prompt generation."""
        content = "def fibonacci(n):"
        command = "complete this function"
        
        prompt = self.manager.get_prompt_for_command(content, command)
        
        assert "Complete the following incomplete content" in prompt
        assert "complete this function" in prompt  # command detail included
        assert "def fibonacci(n):" in prompt
        assert "Completed version:" in prompt
    
    def test_summarize_command_prompt(self):
        """Test summarize command prompt generation."""
        content = "Long article about artificial intelligence and its applications..."
        command = "summarize key points"
        
        prompt = self.manager.get_prompt_for_command(content, command)
        
        assert "Summarize the following text concisely" in prompt
        assert "summarize key points" in prompt  # command detail included
        assert "Long article about artificial intelligence" in prompt
        assert "Summary:" in prompt


class TestConvenienceFunctions:
    """Test suite for convenience functions."""
    
    def test_build_prompt_for_command_function(self):
        """Test build_prompt_for_command convenience function."""
        content = "Hello world"
        command = "translate to french"
        
        prompt = build_prompt_for_command(content, command)
        
        assert "Hello world" in prompt
        assert "translate to french" in prompt
        assert "Translation:" in prompt
    
    def test_build_default_prompt_function(self):
        """Test build_default_prompt convenience function."""
        content = "Helo wrold"
        
        prompt = build_default_prompt(content)
        
        assert "Helo wrold" in prompt
        assert "Fix the syntax and typos" in prompt
    
    def test_get_command_category_function(self):
        """Test get_command_category convenience function."""
        assert get_command_category("translate to spanish") == "translate"
        assert get_command_category("explain this") == "explain"
        assert get_command_category("unknown command") == "generic"


class TestTemplateIntegrity:
    """Test suite to ensure template integrity and consistency."""
    
    def test_all_core_templates_have_placeholders(self):
        """Test that all core templates have required placeholders."""
        for template_type, template in CORE_TEMPLATES.items():
            # All templates should have {text} placeholder
            assert "{text}" in template, f"Template '{template_type}' missing {{text}} placeholder"
            
            # Non-default templates should also have {command_detail} placeholder
            if template_type != 'default':
                assert "{command_detail}" in template, f"Template '{template_type}' missing {{command_detail}} placeholder"
    
    def test_command_categories_match_templates(self):
        """Test that all command categories have corresponding templates."""
        for category in COMMAND_CATEGORIES.values():
            assert category in CORE_TEMPLATES, f"Category '{category}' has no corresponding template"
    
    def test_template_formatting_safety(self):
        """Test that templates can be safely formatted."""
        manager = PromptManager()
        
        for template_type in CORE_TEMPLATES.keys():
            template = manager.get_template(template_type)
            
            try:
                # Should not raise exception with basic content
                formatted = manager.build_prompt(template, "test content", "test command")
                assert len(formatted) > 0
            except Exception as e:
                pytest.fail(f"Template '{template_type}' failed to format: {e}")


if __name__ == "__main__":
    # Run the tests
    pytest.main([__file__, "-v"])