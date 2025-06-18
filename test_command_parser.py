"""
Unit tests for CommandParser class

Tests the functionality of command parsing, extraction, and content cleaning.
"""

import pytest
from command_parser import CommandParser, parse_command, extract_command_simple, clean_text


class TestCommandParser:
    """Test suite for CommandParser class."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.parser = CommandParser()
    
    def test_basic_command_parsing(self):
        """Test basic command parsing functionality."""
        text = "Hello world <#translate to spanish>"
        content, command, has_command = self.parser.parse_clipboard_content(text)
        
        assert has_command is True
        assert command == "translate to spanish"
        assert content == "Hello world"
    
    def test_no_command(self):
        """Test parsing text without commands."""
        text = "Just regular text without any commands"
        content, command, has_command = self.parser.parse_clipboard_content(text)
        
        assert has_command is False
        assert command == ""
        assert content == text
    
    def test_multiple_commands_uses_last(self):
        """Test that multiple commands use the last one found."""
        text = "Fix this <#translate> and also <#explain>"
        content, command, has_command = self.parser.parse_clipboard_content(text)
        
        assert has_command is True
        assert command == "explain"
        assert content == "Fix this and also"
    
    def test_empty_command(self):
        """Test handling of empty commands."""
        text = "Text with empty command <#>"
        content, command, has_command = self.parser.parse_clipboard_content(text)
        
        assert has_command is False
        assert command == ""
        # Since no valid command, return original text
        assert content == text
    
    def test_whitespace_command(self):
        """Test handling of whitespace-only commands."""
        text = "Text with whitespace <#   >"
        content, command, has_command = self.parser.parse_clipboard_content(text)
        
        assert has_command is False
        assert command == ""
        # Since no valid command, return original text
        assert content == text
    
    def test_command_with_extra_whitespace(self):
        """Test command parsing with extra whitespace."""
        text = "Hello <#  translate to french  >"
        content, command, has_command = self.parser.parse_clipboard_content(text)
        
        assert has_command is True
        assert command == "translate to french"
        assert content == "Hello"
    
    def test_command_case_insensitive(self):
        """Test that command parsing is case insensitive."""
        text1 = "Text <#TRANSLATE>"
        text2 = "Text <#translate>"
        text3 = "Text <#TrAnSlAtE>"
        
        _, cmd1, has1 = self.parser.parse_clipboard_content(text1)
        _, cmd2, has2 = self.parser.parse_clipboard_content(text2)
        _, cmd3, has3 = self.parser.parse_clipboard_content(text3)
        
        assert has1 and has2 and has3
        assert cmd1.lower() == cmd2.lower() == cmd3.lower()
    
    def test_command_with_special_characters(self):
        """Test commands containing special characters."""
        text = "Code <#translate to chinese and explain>"
        content, command, has_command = self.parser.parse_clipboard_content(text)
        
        assert has_command is True
        assert command == "translate to chinese and explain"
        assert content == "Code"
    
    def test_malformed_commands(self):
        """Test handling of malformed command syntax."""
        test_cases = [
            ("Text <#incomplete", False),  # Missing closing >
            ("Text incomplete#>", False),  # Missing opening <
            ("Text <incomplete>", False),  # Missing #
            ("Text #incomplete>", False),  # Missing opening <
            ("Text <<#double>>", True),   # Double brackets - actually valid, finds <#double>
        ]
        
        for text, should_have_command in test_cases:
            content, command, has_command = self.parser.parse_clipboard_content(text)
            
            if should_have_command:
                assert has_command is True
                # For the double bracket case, it should extract "double"
                if "double" in text:
                    assert command == "double"
            else:
                assert has_command is False
                assert command == ""
                assert content == text  # Original text should be preserved
    
    def test_nested_brackets(self):
        """Test handling of nested or multiple bracket scenarios."""
        text = "Text with <brackets> and <#real command>"
        content, command, has_command = self.parser.parse_clipboard_content(text)
        
        assert has_command is True
        assert command == "real command"
        assert "Text with <brackets> and" in content
    
    def test_command_at_beginning(self):
        """Test command at the beginning of text."""
        text = "<#translate> This is the text to translate"
        content, command, has_command = self.parser.parse_clipboard_content(text)
        
        assert has_command is True
        assert command == "translate"
        assert content == "This is the text to translate"
    
    def test_command_at_end(self):
        """Test command at the end of text."""
        text = "Translate this text <#to spanish>"
        content, command, has_command = self.parser.parse_clipboard_content(text)
        
        assert has_command is True
        assert command == "to spanish"
        assert content == "Translate this text"
    
    def test_command_only(self):
        """Test text that contains only a command."""
        text = "<#explain>"
        content, command, has_command = self.parser.parse_clipboard_content(text)
        
        assert has_command is True
        assert command == "explain"
        assert content == ""
    
    def test_extract_command_method(self):
        """Test the extract_command method directly."""
        text = "Some text <#test command>"
        command = self.parser.extract_command(text)
        
        assert command == "test command"
    
    def test_extract_command_none(self):
        """Test extract_command returns None when no command found."""
        text = "Text without command"
        command = self.parser.extract_command(text)
        
        assert command is None
    
    def test_has_command_method(self):
        """Test the has_command method."""
        text_with_cmd = "Text <#with command>"
        text_without_cmd = "Text without command"
        
        assert self.parser.has_command(text_with_cmd) is True
        assert self.parser.has_command(text_without_cmd) is False
    
    def test_get_all_commands(self):
        """Test extracting all commands from text."""
        text = "First <#translate> then <#explain> and finally <#summarize>"
        commands = self.parser.get_all_commands(text)
        
        assert len(commands) == 3
        assert commands == ["translate", "explain", "summarize"]
    
    def test_clean_content_method(self):
        """Test the clean_content method directly."""
        text = "Hello <#translate> world <#explain>"
        cleaned = self.parser.clean_content(text)
        
        assert cleaned == "Hello world"
    
    def test_validate_command_valid(self):
        """Test command validation with valid commands."""
        valid_commands = [
            "translate",
            "translate to spanish",
            "fix and explain",
            "complete this function",
        ]
        
        for cmd in valid_commands:
            assert self.parser.validate_command(cmd) is True
    
    def test_validate_command_invalid(self):
        """Test command validation with invalid commands."""
        invalid_commands = [
            "",  # Empty
            "   ",  # Whitespace only
            "a" * 101,  # Too long
            "command with < brackets",  # Dangerous chars
            "command with > brackets",
            "command with | pipe",
            "command with & ampersand",
        ]
        
        for cmd in invalid_commands:
            assert self.parser.validate_command(cmd) is False
    
    def test_edge_cases_empty_and_none(self):
        """Test edge cases with empty and None inputs."""
        # Test with None
        content, command, has_command = self.parser.parse_clipboard_content(None)
        assert content == ""
        assert command == ""
        assert has_command is False
        
        # Test with empty string
        content, command, has_command = self.parser.parse_clipboard_content("")
        assert content == ""
        assert command == ""
        assert has_command is False
    
    def test_whitespace_handling(self):
        """Test proper whitespace handling in content cleaning."""
        text = "  Hello   world  <#translate>  "
        content, command, has_command = self.parser.parse_clipboard_content(text)
        
        assert has_command is True
        assert command == "translate"
        assert content == "Hello world"  # Extra whitespace should be cleaned
    
    def test_real_world_scenarios(self):
        """Test real-world usage scenarios."""
        scenarios = [
            {
                "input": "def fibonacci(n): pass <#complete this function>",
                "expected_content": "def fibonacci(n): pass",
                "expected_command": "complete this function",
                "should_have_command": True,
            },
            {
                "input": "Machine learning is complex <#explain in simple terms>",
                "expected_content": "Machine learning is complex",
                "expected_command": "explain in simple terms",
                "should_have_command": True,
            },
            {
                "input": "Bonjour le monde <#translate to english>",
                "expected_content": "Bonjour le monde",
                "expected_command": "translate to english",
                "should_have_command": True,
            },
            {
                "input": "Just regular text without any commands",
                "expected_content": "Just regular text without any commands",
                "expected_command": "",
                "should_have_command": False,
            },
        ]
        
        for scenario in scenarios:
            content, command, has_command = self.parser.parse_clipboard_content(scenario["input"])
            
            assert content == scenario["expected_content"]
            assert command == scenario["expected_command"]
            assert has_command == scenario["should_have_command"]


class TestConvenienceFunctions:
    """Test suite for convenience functions."""
    
    def test_parse_command_function(self):
        """Test the parse_command convenience function."""
        text = "Hello <#translate>"
        content, command, has_command = parse_command(text)
        
        assert has_command is True
        assert command == "translate"
        assert content == "Hello"
    
    def test_extract_command_simple_function(self):
        """Test the extract_command_simple convenience function."""
        text = "Hello <#translate>"
        command = extract_command_simple(text)
        
        assert command == "translate"
    
    def test_clean_text_function(self):
        """Test the clean_text convenience function."""
        text = "Hello <#translate> world"
        cleaned = clean_text(text)
        
        assert cleaned == "Hello world"


if __name__ == "__main__":
    # Run the tests
    pytest.main([__file__, "-v"])