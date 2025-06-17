#!/usr/bin/env python3
"""
Integration test script for no_more_typo enhanced functionality

This script tests the integration without requiring real LLM API calls
by mocking the LLM responses.
"""

import os
import sys
from unittest.mock import Mock, patch
import pyperclip

# Add current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from enhanced_processor import EnhancedProcessor


def test_enhanced_processor_integration():
    """Test the enhanced processor with mocked LLM."""
    print("🧪 Testing Enhanced Processor Integration")
    print("=" * 50)
    
    # Create mock LLM
    mock_llm = Mock()
    
    # Test cases with expected responses
    test_cases = [
        {
            "input": "Hello world <#translate to spanish>",
            "expected_category": "translate",
            "mock_response": "Hola mundo",
            "description": "Translation command"
        },
        {
            "input": "Machine learning <#explain simply>",
            "expected_category": "explain", 
            "mock_response": "Machine learning is when computers learn from data",
            "description": "Explanation command"
        },
        {
            "input": "def func(): pass <#complete this function>",
            "expected_category": "complete",
            "mock_response": "def func():\n    return 'Hello World'",
            "description": "Code completion command"
        },
        {
            "input": "This code has bugs <#fix errors>",
            "expected_category": "fix",
            "mock_response": "This code has been fixed",
            "description": "Fix command"
        },
        {
            "input": "AI is powerful <#elaborate with examples>",
            "expected_category": "elaborate",
            "mock_response": "AI is powerful technology with applications in healthcare, finance, and education",
            "description": "Elaborate command"
        },
        {
            "input": "Custom task <#make this more formal>",
            "expected_category": "generic",
            "mock_response": "This task has been made more formal",
            "description": "Generic command"
        },
        {
            "input": "Just regular text with typos",
            "expected_category": None,
            "mock_response": "Just regular text without typos",
            "description": "Default typo fixing (no command)"
        }
    ]
    
    # Initialize processor with mock LLM
    processor = EnhancedProcessor(llm=mock_llm)
    
    print(f"✅ Enhanced processor initialized successfully")
    print(f"📋 Available templates: {processor.get_available_commands()}")
    print()
    
    # Test each case
    for i, test_case in enumerate(test_cases, 1):
        print(f"Test {i}: {test_case['description']}")
        print(f"Input: {test_case['input']}")
        
        # Configure mock response
        mock_llm.reset_mock()
        mock_llm.invoke.return_value = test_case['mock_response']
        
        try:
            # Test command categorization if it's a command
            if test_case['expected_category']:
                # Extract command from input
                if '<#' in test_case['input']:
                    command_start = test_case['input'].find('<#') + 2
                    command_end = test_case['input'].find('>', command_start)
                    command = test_case['input'][command_start:command_end]
                    
                    category = processor.get_command_category(command)
                    print(f"Command category: {category}")
                    assert category == test_case['expected_category'], f"Expected {test_case['expected_category']}, got {category}"
            
            # Test processing
            result = processor.process_clipboard_content(test_case['input'])
            print(f"Output: {result}")
            
            # Verify LLM was called appropriately
            if test_case['expected_category']:
                assert mock_llm.invoke.called, "LLM should have been called"
                # Check that the prompt contains expected elements
                call_args = mock_llm.invoke.call_args[0][0]
                assert test_case['input'].replace('<#' + command + '>', '').strip() in call_args
            
            print(f"✅ Test {i} passed")
            
        except Exception as e:
            print(f"❌ Test {i} failed: {e}")
            return False
        
        print()
    
    print("🎉 All integration tests passed!")
    return True


def test_clipboard_simulation():
    """Test clipboard operations simulation."""
    print("📋 Testing Clipboard Operations")
    print("=" * 30)
    
    # Test setting and getting clipboard content
    test_content = "Hello world <#translate to french>"
    
    try:
        pyperclip.copy(test_content)
        retrieved_content = pyperclip.paste()
        
        print(f"Set clipboard: {test_content}")
        print(f"Retrieved: {retrieved_content}")
        
        assert retrieved_content == test_content, "Clipboard operation failed"
        print("✅ Clipboard operations working")
        return True
        
    except Exception as e:
        print(f"❌ Clipboard test failed: {e}")
        print("   Note: Clipboard operations may not work in some environments")
        return False


def test_prompt_generation():
    """Test prompt generation for different commands."""
    print("📝 Testing Prompt Generation")
    print("=" * 30)
    
    processor = EnhancedProcessor(llm=Mock())
    
    test_prompts = [
        ("Hello world", "translate to spanish", "Translate"),
        ("Code bug", "fix this", "Fix"),
        ("Concept", "explain", "Explain"),
        ("Text", "elaborate", "Elaborate"),
        ("Function", "complete", "Complete"),
        ("Article", "summarize", "Summarize"),
        ("Custom", "make formal", "Process")
    ]
    
    for content, command, expected_keyword in test_prompts:
        try:
            prompt = processor.preview_prompt(content, command)
            print(f"Command: {command}")
            print(f"Generated prompt preview: {prompt[:100]}...")
            
            assert expected_keyword.lower() in prompt.lower(), f"Expected '{expected_keyword}' in prompt"
            assert content in prompt, f"Expected content '{content}' in prompt"
            
            print("✅ Prompt generated correctly")
            
        except Exception as e:
            print(f"❌ Prompt generation failed: {e}")
            return False
        
        print()
    
    print("✅ All prompt generation tests passed!")
    return True


def main():
    """Run all integration tests."""
    print("🚀 Starting no_more_typo Integration Tests")
    print("=" * 60)
    print()
    
    tests = [
        ("Enhanced Processor Integration", test_enhanced_processor_integration),
        ("Clipboard Operations", test_clipboard_simulation),
        ("Prompt Generation", test_prompt_generation)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"🧪 Running: {test_name}")
        print("-" * 40)
        
        try:
            if test_func():
                passed += 1
                print(f"✅ {test_name}: PASSED")
            else:
                print(f"❌ {test_name}: FAILED")
        except Exception as e:
            print(f"❌ {test_name}: ERROR - {e}")
        
        print()
    
    print("=" * 60)
    print(f"📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! Integration is working correctly.")
        return True
    else:
        print("⚠️  Some tests failed. Check the output above for details.")
        return False


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)