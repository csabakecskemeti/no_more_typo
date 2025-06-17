# pip install --upgrade pyperclip pynput langchain langchain-openai langchain-community langchain-core
import pyperclip
from pynput import keyboard
from langchain_community.llms.openai import OpenAI
import sys
import os
import warnings

# Import enhanced processing capabilities
from enhanced_processor import EnhancedProcessor

print("""
╔══════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════╗
║                                                                                                                                              ║
║ ▄▄        ▄  ▄▄▄▄▄▄▄▄▄▄▄       ▄▄       ▄▄  ▄▄▄▄▄▄▄▄▄▄▄  ▄▄▄▄▄▄▄▄▄▄▄  ▄▄▄▄▄▄▄▄▄▄▄       ▄▄▄▄▄▄▄▄▄▄▄  ▄         ▄  ▄▄▄▄▄▄▄▄▄▄▄  ▄▄▄▄▄▄▄▄▄▄▄   ║
║▐░░▌      ▐░▌▐░░░░░░░░░░░▌     ▐░░▌     ▐░░▌▐░░░░░░░░░░░▌▐░░░░░░░░░░░▌▐░░░░░░░░░░░▌     ▐░░░░░░░░░░░▌▐░▌       ▐░▌▐░░░░░░░░░░░▌▐░░░░░░░░░░░▌  ║
║▐░▌░▌     ▐░▌▐░█▀▀▀▀▀▀▀█░▌     ▐░▌░▌   ▐░▐░▌▐░█▀▀▀▀▀▀▀█░▌▐░█▀▀▀▀▀▀▀█░▌▐░█▀▀▀▀▀▀▀▀▀       ▀▀▀▀█░█▀▀▀▀ ▐░▌       ▐░▌▐░█▀▀▀▀▀▀▀█░▌▐░█▀▀▀▀▀▀▀█░▌  ║
║▐░▌▐░▌    ▐░▌▐░▌       ▐░▌     ▐░▌▐░▌ ▐░▌▐░▌▐░▌       ▐░▌▐░▌       ▐░▌▐░▌                    ▐░▌     ▐░▌       ▐░▌▐░▌       ▐░▌▐░▌       ▐░▌  ║
║▐░▌ ▐░▌   ▐░▌▐░▌       ▐░▌     ▐░▌ ▐░▐░▌ ▐░▌▐░▌       ▐░▌▐░█▄▄▄▄▄▄▄█░▌▐░█▄▄▄▄▄▄▄▄▄           ▐░▌     ▐░█▄▄▄▄▄▄▄█░▌▐░█▄▄▄▄▄▄▄█░▌▐░▌       ▐░▌  ║
║▐░▌  ▐░▌  ▐░▌▐░▌       ▐░▌     ▐░▌  ▐░▌  ▐░▌▐░▌       ▐░▌▐░░░░░░░░░░░▌▐░░░░░░░░░░░▌          ▐░▌     ▐░░░░░░░░░░░▌▐░░░░░░░░░░░▌▐░▌       ▐░▌  ║
║▐░▌   ▐░▌ ▐░▌▐░▌       ▐░▌     ▐░▌   ▀   ▐░▌▐░▌       ▐░▌▐░█▀▀▀▀█░█▀▀ ▐░█▀▀▀▀▀▀▀▀▀           ▐░▌      ▀▀▀▀█░█▀▀▀▀ ▐░█▀▀▀▀▀▀▀▀▀ ▐░▌       ▐░▌  ║
║▐░▌    ▐░▌▐░▌▐░▌       ▐░▌     ▐░▌       ▐░▌▐░▌       ▐░▌▐░▌     ▐░▌  ▐░▌                    ▐░▌          ▐░▌     ▐░▌          ▐░▌       ▐░▌  ║
║▐░▌     ▐░▐░▌▐░█▄▄▄▄▄▄▄█░▌     ▐░▌       ▐░▌▐░█▄▄▄▄▄▄▄█░▌▐░▌      ▐░▌ ▐░█▄▄▄▄▄▄▄▄▄           ▐░▌          ▐░▌     ▐░▌          ▐░█▄▄▄▄▄▄▄█░▌  ║
║▐░▌      ▐░░▌▐░░░░░░░░░░░▌     ▐░▌       ▐░▌▐░░░░░░░░░░░▌▐░▌       ▐░▌▐░░░░░░░░░░░▌          ▐░▌          ▐░▌     ▐░▌          ▐░░░░░░░░░░░▌  ║
║ ▀        ▀▀  ▀▀▀▀▀▀▀▀▀▀▀       ▀         ▀  ▀▀▀▀▀▀▀▀▀▀▀  ▀         ▀  ▀▀▀▀▀▀▀▀▀▀▀            ▀            ▀       ▀            ▀▀▀▀▀▀▀▀▀▀▀   ║
║                                                                                                                                              ║
║                                                                                                                                              ║
║  ClipIQ - Intelligent Clipboard Processing                                                                                                      ║
║  ClipIQ by devquasar.com - Enhanced AI clipboard assistant with command support for text processing and transformation.                   ║
║                                                                                                                                              ║
║  LLM api_key should be available in the OPENAI_API_KEY environment variable.                                                                 ║
║  To use custom default template export it to the NO_MORE_TYPO_PROMPT_TEMPLATE environment variable                                          ║
║                                                                                                                                              ║
║  USAGE:                                                                                                                                      ║
║    Regular text                     → Fixes typos and syntax                                                                                 ║
║    "Text <#translate to spanish>"   → Translates text to Spanish                                                                            ║
║    "Code <#fix errors>"            → Fixes code errors                                                                                      ║
║    "Concept <#explain simply>"     → Explains in simple terms                                                                               ║
║    "Text <#elaborate>"             → Adds more detail                                                                                       ║
║    "Function <#complete>"          → Completes code                                                                                         ║
║    "Article <#summarize>"          → Summarizes content                                                                                     ║
║    "Custom <#any instruction>"     → Follows any instruction                                                                                ║
║                                                                                                                                              ║
║  Activate processing: [ctrl]+[shift]+[z]                                                                                                    ║
║  Exit app: [ctrl]+[shift]+[x]                                                                                                                ║
║                                                                                                                                              ║
║  2024 devquasar.com                                                                                                                          ║
║                                                                                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════╝
""")


# Suppress all warnings
warnings.filterwarnings("ignore")

# Initialize the enhanced processor
print("Initializing ClipIQ - Intelligent Clipboard Processing...")
try:
    llm = OpenAI()
    enhanced_processor = EnhancedProcessor(llm=llm)
    print("✅ ClipIQ processor ready with command support!")
    print("   • Use <#command> syntax for intelligent processing")
    print("   • Regular text will be processed for typos (backward compatible)")
    print("   • Powered by AI for instant text transformation")
    print()
except Exception as e:
    print(f"❌ Failed to initialize enhanced processor: {e}")
    print("   Falling back to basic typo fixing...")
    
    # Fallback to original implementation
    from langchain_core.prompts import PromptTemplate
    from langchain.schema.runnable import RunnableLambda
    
    default_prompt = "Fix the syntax and typos text:\n\n{text}\n\nThe correct string is:"
    custom_prompt = os.getenv("NO_MORE_TYPO_PROMPT_TEMPLATE", default_prompt)
    
    if "{text}" not in custom_prompt:
        custom_prompt += "\n CONTEXT: \n {text}"
    
    prompt = PromptTemplate.from_template(custom_prompt)
    cleanup = RunnableLambda(lambda x: x.strip().strip('"').strip("'"))
    no_typo_chain = prompt | llm | cleanup
    enhanced_processor = None


def on_activate():
    """Process clipboard content with enhanced AI capabilities."""
    try:
        original_clipboard_content = pyperclip.paste()
        
        if not original_clipboard_content:
            print("⚠️  Clipboard is empty")
            return
        
        print(f"📝 Processing: {original_clipboard_content[:50]}{'...' if len(original_clipboard_content) > 50 else ''}")
        
        if enhanced_processor:
            # Use enhanced processor with command support
            processed_content = enhanced_processor.process_clipboard_content(original_clipboard_content)
        else:
            # Fallback to original implementation
            processed_content = no_typo_chain.invoke({"text": original_clipboard_content})
        
        pyperclip.copy(processed_content)
        print(f"✅ Processed and copied to clipboard")
        print(f"📋 Result: {processed_content[:100]}{'...' if len(processed_content) > 100 else ''}")
        print()
        
    except Exception as e:
        print(f"❌ Processing failed: {e}")
        print("   Original content remains in clipboard")
        print()


def on_exit():
    """Exit the application gracefully."""
    print("👋 Exiting no_more_typo app...")
    if enhanced_processor:
        print("   Enhanced AI processor shut down")
    print("   Goodbye!")
    sys.exit(0)


def print_help():
    """Print help information about available commands."""
    print("🧠 ClipIQ - INTELLIGENT COMMANDS:")
    print("   <#translate to [language]>   - Translate text")
    print("   <#explain>                   - Explain concept simply") 
    print("   <#fix>                       - Fix errors/bugs")
    print("   <#elaborate>                 - Add more detail")
    print("   <#complete>                  - Complete code/text")
    print("   <#summarize>                 - Create summary")
    print("   <#[any instruction]>         - Custom processing")
    print()
    print("   Examples:")
    print("   • 'Hola mundo <#translate to english>'")
    print("   • 'def func(): pass <#complete this function>'")
    print("   • 'Machine learning <#explain simply>'")
    print()
    print("   📄 ClipIQ by devquasar.com - evolved from no_more_typo!")
    print()


# Print startup help
print_help()

print("🎯 Ready! Press Ctrl+Shift+Z to process clipboard content")
print("   Press Ctrl+Shift+X to exit")
print()

# Set up global hotkeys
try:
    with keyboard.GlobalHotKeys(
        {
            '<ctrl>+<shift>+z': on_activate,
            '<ctrl>+<shift>+x': on_exit
        }
    ) as h:
        h.join()
except KeyboardInterrupt:
    print("\n👋 Received interrupt signal, exiting...")
    sys.exit(0)
except Exception as e:
    print(f"❌ Failed to start hotkey listener: {e}")
    print("   Please check if another instance is running")
    sys.exit(1)
