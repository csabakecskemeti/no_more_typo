# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**ClipIQ** (formerly no_more_typo) is an enhanced AI-powered clipboard assistant that uses LLM (OpenAI) for intelligent text processing and transformation. Beyond simple typo fixing, it now supports sophisticated command-based processing for translation, explanation, code completion, and custom text transformations. The application runs as a background service with global hotkeys for activation.

**Transitional Branding**: The project maintains the "no_more_typo" technical name for backward compatibility while introducing "ClipIQ" as the user-facing brand for intelligent clipboard processing.

## Architecture

- **Main Application**: `no_more_typo.py` - Enhanced AI clipboard assistant with command support
- **Core Components**:
  - `enhanced_processor.py` - Main processing pipeline with command handling
  - `command_parser.py` - Parses `<#command>` syntax from clipboard text
  - `prompt_templates.py` - Hardcoded core templates for different command types
  - LangChain integration with OpenAI LLM
  - Clipboard manipulation via pyperclip
  - Global hotkey handling via pynput
- **Distribution**: PyInstaller creates standalone executable in `dist/` folder

## Command System

### Command Syntax
Use `<#command>` syntax to specify processing instructions:
```
"Regular text"                          → Typo fixing (backward compatible)
"Hello world <#translate to spanish>"   → Translation
"def func(): pass <#complete>"          → Code completion
"Complex topic <#explain simply>"       → Simple explanation
"Short text <#elaborate>"               → Add more detail
"Buggy code <#fix errors>"             → Fix issues
"Long article <#summarize>"             → Create summary
"Any text <#custom instruction>"        → Generic processing
```

### Supported Commands
- **translate** - Translate text to specified language
- **explain** - Explain concepts in simple terms
- **fix** - Fix errors, bugs, or issues
- **elaborate** - Expand text with more detail
- **complete** - Complete incomplete code/text
- **summarize** - Create concise summaries
- **Generic** - Any other instruction (uses flexible template)

## Development Setup

### Virtual Environment Setup
```bash
# Create virtual environment
python -m venv .venv

# Activate virtual environment
# On macOS/Linux:
source .venv/bin/activate
# On Windows:
# .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Dependencies Installation (Alternative)
```bash
pip install --upgrade pyperclip pynput langchain langchain-openai langchain-community langchain-core pytest pytest-mock
```

### Running the Application
```bash
# Run in foreground (for development/testing)
python no_more_typo.py

# Run in background (recommended for normal use)
python no_more_typo.py&
```

### Testing
```bash
# Run all unit tests
pytest test_*.py -v

# Run integration tests
python test_integration.py

# Run specific test modules
pytest test_command_parser.py -v
pytest test_prompt_templates.py -v
pytest test_enhanced_processor.py -v
```

### Building Executable
```bash
pyinstaller --onefile no_more_typo.py
```

## Environment Variables

- `OPENAI_API_KEY` (required): OpenAI API key for LLM access
- `OPENAI_API_BASE` (optional): Custom OpenAI API base URL
- `NO_MORE_TYPO_PROMPT_TEMPLATE` (optional): Custom default template for text without commands (must include `{text}` placeholder)

**Note**: Only the default template can be customized. Core command templates (translate, explain, fix, etc.) are hardcoded for reliability and cannot be overridden.

## Application Controls

- **Activate processing**: Ctrl+Shift+Z (processes clipboard content with command support)
- **Exit application**: Ctrl+Shift+X

## Key Implementation Details

### Enhanced Processing Pipeline
```
Clipboard Content → Command Parser → Template Selection → LLM Processing → Response Cleanup → Clipboard
```

### Command Processing Flow
1. **Parse**: Extract command from `<#command>` syntax
2. **Categorize**: Determine template type (translate, explain, fix, etc.)
3. **Template**: Select appropriate hardcoded template
4. **Process**: Send structured prompt to LLM
5. **Cleanup**: Remove quotes and normalize whitespace
6. **Output**: Replace clipboard with processed result

### Backward Compatibility
- Text without commands uses traditional typo-fixing behavior
- Existing `NO_MORE_TYPO_PROMPT_TEMPLATE` environment variable still works
- Original hotkeys and functionality preserved

### Error Handling
- Command processing failures fall back to default typo fixing
- Complete processing failures preserve original clipboard content
- Graceful degradation ensures application always functions

### Security Features
- Core templates are hardcoded and cannot be modified by users
- Command validation prevents malicious input
- Safe fallback mechanisms prevent application crashes