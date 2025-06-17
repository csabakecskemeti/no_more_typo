#!/bin/bash

# ClipIQ Build Script
# Builds standalone executable with intelligent clipboard processing

echo "🚀 Building ClipIQ - Intelligent Clipboard Processing..."
echo "   (formerly no_more_typo, now with AI command support)"
echo ""

# Check if virtual environment exists
if [ ! -d ".venv" ]; then
    echo "❌ Virtual environment not found. Please run:"
    echo "   python -m venv .venv"
    echo "   source .venv/bin/activate"
    echo "   pip install -r requirements.txt"
    exit 1
fi

# Activate virtual environment
echo "📦 Activating virtual environment..."
source .venv/bin/activate

# Check if PyInstaller is available
if ! command -v pyinstaller &> /dev/null; then
    echo "❌ PyInstaller not found. Installing..."
    pip install pyinstaller
fi

# Clean previous builds
echo "🧹 Cleaning previous builds..."
rm -rf build/
rm -rf dist/

# Build executable
echo "🔨 Building ClipIQ executable..."
pyinstaller clipiq.spec

# Check if build was successful
if [ -f "dist/clipiq" ]; then
    echo ""
    echo "✅ ClipIQ build successful!"
    echo "   📁 Executable: dist/clipiq"
    echo "   📊 Size: $(du -h dist/clipiq | cut -f1)"
    echo ""
    echo "🧠 ClipIQ Features:"
    echo "   • Intelligent command processing with <#command> syntax"
    echo "   • Universal app compatibility (works everywhere)"
    echo "   • Backward compatible with original no_more_typo"
    echo "   • 96+ tests for production reliability"
    echo ""
    echo "🎯 To test:"
    echo "   export OPENAI_API_KEY='your-key-here'"
    echo "   ./dist/clipiq"
    echo ""
    echo "📦 Distribution ready! ClipIQ intelligence in 34MB."
else
    echo ""
    echo "❌ Build failed! Check the output above for errors."
    exit 1
fi