#!/usr/bin/env python3
"""
Simple test to verify our modules can be imported
"""

def test_imports():
    """Test that all our modules can be imported correctly."""
    print("🧪 Testing Module Imports")
    print("=" * 30)
    
    modules_to_test = [
        ("command_parser", "CommandParser"),
        ("prompt_templates", "PromptManager"),
        ("enhanced_processor", "EnhancedProcessor"),
    ]
    
    for module_name, class_name in modules_to_test:
        try:
            module = __import__(module_name)
            cls = getattr(module, class_name)
            print(f"✅ {module_name}.{class_name}")
        except Exception as e:
            print(f"❌ {module_name}.{class_name}: {e}")
            return False
    
    print("\n🧪 Testing Enhanced Processor Functionality")
    print("=" * 40)
    
    try:
        from unittest.mock import Mock
        from enhanced_processor import EnhancedProcessor
        
        # Create processor with mock LLM
        mock_llm = Mock()
        mock_llm.invoke.return_value = "Test response"
        
        processor = EnhancedProcessor(llm=mock_llm)
        
        # Test command parsing
        result = processor.process_clipboard_content("Hello world <#translate to spanish>")
        print(f"✅ Command processing: {result}")
        
        # Test default processing
        result = processor.process_clipboard_content("Regular text")
        print(f"✅ Default processing works")
        
        return True
        
    except Exception as e:
        print(f"❌ Enhanced processor test failed: {e}")
        return False

if __name__ == "__main__":
    if test_imports():
        print("\n🎉 All tests passed! The application should work correctly.")
    else:
        print("\n❌ Some tests failed. Check the errors above.")