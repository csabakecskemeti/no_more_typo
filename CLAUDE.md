# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a Python utility called "no_more_typo" that uses LLM (OpenAI) to fix typos and syntax errors in clipboard text. The application runs as a background service with global hotkeys for activation.

## Architecture

- **Main Application**: `no_more_typo.py` - Single-file Python application using langchain for LLM integration
- **Core Components**:
  - LangChain integration with OpenAI LLM
  - Clipboard manipulation via pyperclip
  - Global hotkey handling via pynput
  - Customizable prompt templates via environment variables
- **Distribution**: PyInstaller creates standalone executable in `dist/` folder

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
pip install --upgrade pyperclip pynput langchain langchain-openai langchain-community langchain-core
```

### Running the Application
```bash
# Run in foreground (for development/testing)
python no_more_typo.py

# Run in background (recommended for normal use)
python no_more_typo.py&
```

### Building Executable
```bash
pyinstaller --onefile no_more_typo.py
```

## Environment Variables

- `OPENAI_API_KEY` (required): OpenAI API key for LLM access
- `OPENAI_API_BASE` (optional): Custom OpenAI API base URL
- `NO_MORE_TYPO_PROMPT_TEMPLATE` (optional): Custom prompt template (must include `{text}` placeholder)

## Application Controls

- **Activate fix**: Ctrl+Shift+Z (processes clipboard content)
- **Exit application**: Ctrl+Shift+X

## Key Implementation Details

- The application creates a LangChain pipeline: `prompt | llm | cleanup`
- Default prompt: "Fix the syntax and typos text:\n\n{text}\n\nThe correct string is:"
- Response cleanup removes extra quotes and whitespace
- Global hotkeys work system-wide when application is running