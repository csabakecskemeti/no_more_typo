# Detailed Implementation Plan - no_more_typo Enhanced

## Implementation Order
1. **Phase 1**: Command System (`<#command>` syntax)
2. **Phase 2**: Intent Detection (automatic context understanding)
3. **Phase 3**: Multimodal Vision (screenshots + vision models)
4. **Phase 4**: MCP Agent Integration (desktop assistant capabilities)

---

## Phase 1: Command System Implementation

### Command Syntax Design
**Format**: `<#command_instruction>`
**Examples**:
- `"Hello world <#translate to chinese>"`
- `"This code is buggy <#fix and explain>"`
- `"Machine learning <#elaborate>"`
- `"def fibonacci(n): <#complete this function>"`

### 1.1 Command Parser Component

**File**: `command_parser.py`
```python
class CommandParser:
    def parse_clipboard_content(self, text: str) -> tuple[str, str, bool]
        # Returns: (content, command, has_command)
    
    def extract_command(self, text: str) -> str | None
        # Extracts command from <#...> syntax
    
    def clean_content(self, text: str) -> str
        # Removes command from original text
```

**Implementation Details**:
- Regex pattern: `<#([^>]+)>`
- Support multiple commands in one text (use last one found)
- Case-insensitive command parsing
- Trim whitespace from commands

### 1.2 Command Prompt Templates

**File**: `prompt_templates.py`
```python
COMMAND_TEMPLATES = {
    "default": "Fix the syntax and typos text:\n\n{text}\n\nThe correct string is:",
    "translate": "Translate the following text {command_detail}:\n\n{text}\n\nTranslation:",
    "elaborate": "Elaborate and expand on the following text with more detail:\n\n{text}\n\nElaborated version:",
    "explain": "Explain the following text in simple terms:\n\n{text}\n\nExplanation:",
    "fix": "Fix any errors or issues in the following:\n\n{text}\n\nFixed version:",
    "complete": "Complete the following incomplete content:\n\n{text}\n\nCompleted version:",
    "summarize": "Summarize the following text concisely:\n\n{text}\n\nSummary:",
    "generic": "Process the following text according to this instruction: {command_detail}\n\n{text}\n\nResult:"
}
```

**Command Mapping Logic**:
- Extract command keywords: `translate`, `elaborate`, `explain`, `fix`, `complete`, `summarize`
- If no keyword match → use `generic` template with full command as instruction
- Support compound commands: `"fix and explain"` → use `generic` template

### 1.3 Enhanced Processing Pipeline

**File**: `enhanced_processor.py`
```python
class EnhancedProcessor:
    def __init__(self):
        self.command_parser = CommandParser()
        self.prompt_manager = PromptManager()
        self.llm_chain = self.setup_llm_chain()
    
    def process_clipboard_content(self, clipboard_text: str) -> str:
        # Main processing pipeline
        content, command, has_command = self.command_parser.parse_clipboard_content(clipboard_text)
        
        if has_command:
            return self.process_with_command(content, command)
        else:
            return self.process_default(content)
    
    def process_with_command(self, content: str, command: str) -> str:
        template = self.prompt_manager.get_template_for_command(command)
        prompt = self.build_prompt(template, content, command)
        return self.llm_chain.invoke(prompt)
    
    def process_default(self, content: str) -> str:
        # Current typo-fixing functionality
        return self.original_no_typo_chain.invoke(content)
```

### 1.4 Configuration Updates

**Environment Variables**:
```bash
# Vision model configuration (for Phase 3)
NO_MORE_TYPO_VISION_MODEL=gpt-4-vision-preview  # or claude-3-sonnet, etc.
NO_MORE_TYPO_USE_VISION_FOR_TEXT=false  # Use vision model for text-only tasks

# Command system configuration
NO_MORE_TYPO_COMMAND_SYNTAX=<#...>  # Allow customization of command syntax
NO_MORE_TYPO_MAX_COMMAND_LENGTH=100  # Limit command length
```

### 1.5 Integration with Main Application

**Updates to `no_more_typo.py`**:
```python
# Replace the simple chain
# OLD: no_typo_chain = prompt | llm | cleanup
# NEW: enhanced_processor = EnhancedProcessor()

def on_activate():
    original_clipboard_content = pyperclip.paste()
    processed_content = enhanced_processor.process_clipboard_content(original_clipboard_content)
    pyperclip.copy(processed_content)
```

### 1.6 Testing Strategy

**Test Cases**:
1. **No Command**: Regular text → typo fixing (preserve existing behavior)
2. **Single Commands**: 
   - `"Hello <#translate to spanish>"`
   - `"This is confusing <#explain>"`
   - `"def func(): <#complete>"`
3. **Multiple Commands**: Use last command found
4. **Invalid Commands**: Fallback to default processing
5. **Edge Cases**: Empty commands, malformed syntax, very long commands

**Test File**: `test_command_system.py`

---

## Phase 2: Intent Detection (Future)

### 2.1 Content Type Detection
- **Code Detection**: Language identification (Python, JavaScript, etc.)
- **Terminal Output**: Error pattern recognition
- **Regular Text**: Default to current behavior
- **Documentation**: Technical vs. general text

### 2.2 Automatic Intent Inference
- **Error Messages** → Automatic "fix" intent
- **Incomplete Code** → Automatic "complete" intent
- **Technical Terms** → Option to "explain"

---

## Phase 3: Multimodal Vision (Future)

### 3.1 Screenshot Capture
- **Hotkey**: Ctrl+Shift+S
- **Area Selection**: Click and drag to select screen region
- **OCR Fallback**: If vision model unavailable

### 3.2 Vision Model Integration
- **Model Selection**: gpt-4-vision, claude-3-sonnet, etc.
- **Dual Mode**: Vision model for images, text model for text
- **Unified Mode**: Single vision model for both

---

## Implementation Tasks for Phase 1

### Sprint 1: Core Command Parser (1-2 days)
1. Create `command_parser.py` with regex-based parsing
2. Write unit tests for command extraction
3. Handle edge cases (malformed commands, multiple commands)

### Sprint 2: Prompt Templates (1 day)
1. Create `prompt_templates.py` with command templates
2. Implement command-to-template mapping logic
3. Add generic template for unmapped commands

### Sprint 3: Enhanced Processor (2-3 days)
1. Create `enhanced_processor.py` with new pipeline
2. Integrate command parser and prompt templates
3. Maintain backward compatibility with existing functionality

### Sprint 4: Integration & Testing (1-2 days)
1. Update main `no_more_typo.py` to use enhanced processor
2. Create comprehensive test suite
3. Test with real-world scenarios

### Sprint 5: Configuration & Documentation (1 day)
1. Add new environment variables
2. Update CLAUDE.md with new functionality
3. Create user documentation for command syntax

---

## Success Criteria for Phase 1

1. ✅ **Backward Compatibility**: Existing users see no change in behavior
2. ✅ **Command Recognition**: 95%+ accuracy in detecting `<#command>` syntax
3. ✅ **Template Mapping**: Correct template selection for known commands
4. ✅ **Generic Handling**: Unknown commands use generic template appropriately
5. ✅ **Performance**: <500ms additional processing time for command parsing
6. ✅ **Error Handling**: Graceful fallback when command processing fails

---

## Phase 4: MCP Agent Integration (Future)

### 4.1 Agent Architecture

**Vision**: Transform clipboard processor into desktop AI assistant with action capabilities

**Core Concept**: 
- User copies text or takes screenshot
- AI detects if action is needed (not just text processing)
- Agent uses MCP tools to perform desktop actions
- Results returned to clipboard or executed directly

### 4.2 MCP Integration Design

**MCP Client Setup**:
```python
# New file: mcp_client.py
class MCPClient:
    def __init__(self):
        self.available_tools = {}
        self.active_servers = []
    
    def discover_tools(self) -> dict:
        # Discover available MCP tools from connected servers
    
    def execute_tool(self, tool_name: str, params: dict) -> any:
        # Execute MCP tool with parameters
    
    def is_action_request(self, text: str, command: str) -> bool:
        # Determine if request requires action vs text processing
```

**Agent Decision Engine**:
```python
class AgentDecisionEngine:
    def should_use_agent(self, content: str, command: str) -> bool:
        # Detect action keywords: "create file", "open browser", "search", etc.
    
    def plan_actions(self, content: str, command: str) -> list[dict]:
        # Plan sequence of MCP tool calls needed
    
    def execute_plan(self, action_plan: list[dict]) -> str:
        # Execute actions and return results
```

### 4.3 Action Categories

**File System Operations**:
- `"Create a new Python file with this code <#save as main.py>"`
- `"Open the folder containing this file <#open directory>"`
- `"Search for files containing this error <#find in project>"`

**Web & Research**:
- `"This error message <#search for solution>"`
- `"Open documentation for this API <#open docs>"`
- `"Find examples of this code pattern <#search examples>"`

**Development Tools**:
- `"Run this command in terminal <#execute>"`
- `"Install these dependencies <#install packages>"`
- `"Create git commit with this message <#git commit>"`

**System Integration**:
- `"Send this as email <#compose email>"`
- `"Add this to calendar <#schedule meeting>"`
- `"Take note of this <#save to notes>"`

### 4.4 Enhanced Command System for Actions

**Extended Command Syntax**:
```
# Text processing (current)
"Fix this code <#fix>"

# Actions (new)
"Save this code <#save as utils.py>"
"Search for this error <#web search>"
"Run this command <#execute in terminal>"
"Open this URL <#browse>"
```

**Agent-Aware Prompt Templates**:
```python
AGENT_TEMPLATES = {
    "save_file": "I need to save the following content to a file. Determine appropriate filename and format:\n\n{text}",
    "web_search": "Search for information about: {text}",
    "execute_command": "Execute this command safely: {text}",
    "open_resource": "Open/access this resource: {text}",
}
```

### 4.5 MCP Server Integrations

**Recommended MCP Servers**:
```bash
# File system operations
mcp-server-filesystem

# Web browsing and search
mcp-server-web
mcp-server-brave-search

# Development tools
mcp-server-git
mcp-server-terminal

# Productivity
mcp-server-calendar
mcp-server-email
mcp-server-notes
```

**Configuration**:
```bash
# MCP Configuration
NO_MORE_TYPO_MCP_ENABLED=true
NO_MORE_TYPO_MCP_SERVERS=filesystem,web,git,terminal
NO_MORE_TYPO_AGENT_MODE=ask  # ask, auto, disabled
NO_MORE_TYPO_SAFE_MODE=true  # Require confirmation for destructive actions
```

### 4.6 User Experience for Agent Mode

**Action Confirmation Flow**:
1. User: `"rm -rf node_modules <#execute>"`
2. Agent detects potentially destructive command
3. Shows confirmation: "Execute: rm -rf node_modules? [y/N]"
4. User confirms → Action executed
5. Result copied to clipboard: "✅ Deleted node_modules directory"

**Smart Action Detection**:
```python
# Examples of automatic agent activation
"https://github.com/user/repo"  # → Detect URL, offer to open/clone
"pip install pandas numpy"      # → Detect install command, offer to execute
"File not found: config.json"   # → Detect error, offer to create file
"def calculate_tax(income):"    # → Detect code, offer to save to file
```

### 4.7 Integration with Existing Phases

**Phase 1 + Agent**: Commands can trigger actions
```python
def process_with_command(self, content: str, command: str) -> str:
    if self.agent_engine.should_use_agent(content, command):
        return self.agent_engine.execute_action(content, command)
    else:
        return self.process_text_command(content, command)
```

**Phase 3 + Agent**: Screenshots can trigger actions
```python
# Screenshot of file browser → "Open this directory"
# Screenshot of error → "Search for solution and open first result"
# Screenshot of code → "Save this code to file"
```

### 4.8 Implementation Tasks for Phase 4

**Sprint 1: MCP Client Foundation**
1. Set up MCP client connectivity
2. Tool discovery and registration
3. Basic tool execution framework

**Sprint 2: Agent Decision Engine**
1. Action detection logic
2. Safety checks and confirmations
3. Action planning and execution

**Sprint 3: Integration with Command System**
1. Extend command parser for action commands
2. Agent-aware processing pipeline
3. Fallback to text processing when appropriate

**Sprint 4: User Experience & Safety**
1. Confirmation dialogs for risky actions
2. Action logging and undo capabilities
3. Configuration options for agent behavior

### 4.9 Example Usage Scenarios

**Development Workflow**:
```
User copies: "def fibonacci(n): pass <#complete and save>"
→ AI completes function
→ Agent saves to fibonacci.py
→ Clipboard: "✅ Saved completed fibonacci function to fibonacci.py"
```

**Error Resolution**:
```
User screenshots terminal error
→ AI detects "ModuleNotFoundError: No module named 'requests'"
→ Agent searches for solution
→ Agent executes: "pip install requests"
→ Clipboard: "✅ Installed missing module 'requests'"
```

**Research & Documentation**:
```
User copies: "React useEffect hook <#find examples and open docs>"
→ Agent searches for useEffect examples
→ Agent opens React documentation
→ Clipboard: "📚 Opened React useEffect documentation and found 5 examples"
```

---

## Technical Architecture Changes

### New File Structure:
```
no_more_typo/
├── no_more_typo.py           # Main application (updated)
├── command_parser.py         # NEW: Command parsing logic
├── prompt_templates.py       # NEW: Template management
├── enhanced_processor.py     # NEW: Enhanced processing pipeline
├── mcp_client.py            # NEW: MCP client integration (Phase 4)
├── agent_engine.py          # NEW: Agent decision engine (Phase 4)
├── test_command_system.py    # NEW: Test suite
├── requirements.txt          # Updated with new dependencies
└── CLAUDE.md                # Updated documentation
```

### New Dependencies:
```
# Already have: pyperclip, pynput, langchain, langchain-openai, langchain-community, langchain-core
# Add for testing:
pytest
pytest-mock

# Add for MCP integration (Phase 4):
mcp
asyncio
aiohttp
```

Ready to start with Sprint 1 (Command Parser)? This gives us a solid foundation that we can build the intent detection and vision capabilities on top of later.