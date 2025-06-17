# no_more_typo - Enhanced AI Clipboard Assistant

**Download the standalone executable and start using AI-powered text processing instantly!**

## 🚀 Quick Start

### 1. Download
Download the `no_more_typo` executable from the releases section.

### 2. Set API Key
```bash
export OPENAI_API_KEY="your-openai-api-key-here"
```

### 3. Run
```bash
./no_more_typo
```

### 4. Use
- **Process clipboard**: Press `Ctrl+Shift+Z`
- **Exit application**: Press `Ctrl+Shift+X`

## ✨ Features

### Command-Based Processing
Use `<#command>` syntax for specific AI tasks:

```
"Hello world <#translate to spanish>"     → "Hola mundo"
"def func(): pass <#complete>"            → Complete function code
"Machine learning <#explain simply>"     → Simple explanation
"Buggy code <#fix errors>"              → Fixed code
"Short text <#elaborate>"                → Detailed expansion
"Long article <#summarize>"              → Concise summary
"Any task <#custom instruction>"         → Custom processing
```

### Backward Compatible
Regular text without commands gets typo/grammar fixing:
```
"Helo wrold with typos"  → "Hello world with typos"
```

## 📋 Supported Commands

| Command | Description | Example |
|---------|-------------|---------|
| `<#translate to [lang]>` | Translate text | `<#translate to french>` |
| `<#explain>` | Explain simply | `<#explain in simple terms>` |
| `<#fix>` | Fix errors/bugs | `<#fix syntax errors>` |
| `<#elaborate>` | Add more detail | `<#elaborate with examples>` |
| `<#complete>` | Complete code/text | `<#complete this function>` |
| `<#summarize>` | Create summary | `<#summarize key points>` |
| `<#[anything]>` | Custom instruction | `<#make this more formal>` |

## 🛠️ Requirements

- **Platform**: macOS (ARM64/Intel)
- **API Key**: OpenAI API key required
- **No Python**: Self-contained executable!

## 📖 Usage Examples

### Code Development
```bash
# Copy this to clipboard:
def fibonacci(n): <#complete this recursive function>

# Press Ctrl+Shift+Z, get:
def fibonacci(n):
    if n <= 1:
        return n
    return fibonacci(n-1) + fibonacci(n-2)
```

### Translation
```bash
# Copy: "Bonjour le monde <#translate to english>"
# Get: "Hello world"
```

### Learning & Explanation
```bash
# Copy: "Quantum computing <#explain like I'm 5>"
# Get: Simple explanation suitable for beginners
```

### Code Debugging
```bash
# Copy: "print('hello' <#fix this syntax error>"
# Get: "print('hello')"
```

## ⚙️ Configuration

### Custom Default Template
Set custom template for text without commands:
```bash
export NO_MORE_TYPO_PROMPT_TEMPLATE="Improve this text:\n\n{text}\n\nImproved version:"
```

### Custom OpenAI Endpoint
```bash
export OPENAI_API_BASE="https://your-custom-endpoint.com"
```

## 🔧 Troubleshooting

### "Command not found" or Permission Error
```bash
chmod +x no_more_typo
./no_more_typo
```

### "API Key not found"
Make sure to set your OpenAI API key:
```bash
export OPENAI_API_KEY="sk-your-key-here"
echo $OPENAI_API_KEY  # Verify it's set
```

### Application Won't Start
1. Check you have an internet connection
2. Verify your API key is valid
3. Try running from terminal to see error messages

### Hotkeys Don't Work
- Make sure no other application is using the same hotkeys
- On macOS, you might need to grant accessibility permissions
- Try running as administrator if needed

## 📊 Technical Details

- **Size**: ~34 MB (includes all dependencies)
- **Startup Time**: 2-3 seconds first run
- **Processing Time**: 1-5 seconds depending on text length
- **Memory Usage**: ~100-200 MB during operation

## 🔒 Security & Privacy

- **API Keys**: Stored only in environment variables
- **Core Templates**: Hardcoded and cannot be modified
- **Text Processing**: Sent to OpenAI API (follows their privacy policy)
- **No Data Storage**: No text is stored locally

## 🆘 Support

- **Issues**: Report problems on GitHub
- **Feature Requests**: Open an issue with enhancement label
- **Documentation**: Check CLAUDE.md for development details

## 📄 License

This project is open source. See LICENSE file for details.

---

**Enjoy your enhanced AI clipboard assistant! 🎉**