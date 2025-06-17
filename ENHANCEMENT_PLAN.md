# no_more_typo Enhancement Plan

## Vision
Transform the simple typo-fixing utility into an intelligent, context-aware clipboard AI assistant that understands user intent and provides appropriate assistance.

## Current Functionality
- Fixes typos/syntax in clipboard text via Ctrl+Shift+Z
- Uses LangChain + OpenAI LLM
- Customizable prompt templates

## Proposed Enhancements

### 1. Screenshot Text Extraction
**Goal**: Capture and process text from screenshots
- **Trigger**: Print Screen or new hotkey (e.g., Ctrl+Shift+S)
- **Process**: Screenshot → OCR → Text extraction → Intent detection → AI processing
- **Use Cases**:
  - Terminal errors → Get fix suggestions
  - Code snippets → Complete/fix code
  - Documentation → Summarize/explain

### 2. Context-Aware Intent Detection
**Goal**: Understand what user wants based on content type and context

**Content Types to Detect**:
- **Terminal/Command Line Output**:
  - Error messages → Provide fixes with comments + commands
  - Incomplete commands → Complete them
- **Code Snippets**:
  - Buggy code → Fix and complete
  - Incomplete code → Complete implementation
- **Regular Text**:
  - Keep current typo/syntax fixing
- **Documentation/Articles**:
  - Summarize or explain based on intent

### 3. Command Modifiers
**Goal**: Allow users to specify intent explicitly
- **#elaborate** - Expand and add more detail
- **#explain** - Provide explanation/breakdown
- **#fix** - Focus on fixing errors/issues
- **#complete** - Complete incomplete code/commands
- **#summarize** - Create concise summary

### 4. Enhanced Processing Pipeline
**Current**: `prompt | llm | cleanup`
**Proposed**: `input | content_detector | intent_detector | prompt_selector | llm | formatter | output`

## Implementation Phases

### Phase 1: Core Architecture Refactor
**Deliverables**:
- Content type detection system
- Intent detection framework
- Multiple prompt templates
- Enhanced processing pipeline

**Technical Requirements**:
- Content analysis utilities
- Prompt template management
- Processing pipeline refactor

### Phase 2: Command Modifiers
**Deliverables**:
- Command parsing (#elaborate, #explain, etc.)
- Command-specific prompt templates
- Enhanced user interface feedback

**Technical Requirements**:
- Regex/parsing for commands
- Command-to-prompt mapping
- Testing for various command combinations

### Phase 3: Screenshot Integration
**Deliverables**:
- Screenshot capture functionality
- OCR text extraction
- Screenshot-specific processing pipeline

**Technical Requirements**:
- Screenshot library (pillow, pyautogui)
- OCR library (pytesseract, easyocr)
- Image preprocessing
- New hotkey binding

### Phase 4: Advanced Context Detection
**Deliverables**:
- Terminal error pattern recognition
- Code language detection
- Smart formatting for different content types

**Technical Requirements**:
- Pattern matching for common error formats
- Language detection utilities
- Context-specific formatting

## Technical Architecture

### New Components Needed:
1. **ContentDetector**: Identifies content type (code, terminal, text, etc.)
2. **IntentDetector**: Determines user intent from content + commands
3. **PromptManager**: Manages multiple prompt templates
4. **ScreenshotCapture**: Handles screenshot + OCR
5. **CommandParser**: Parses user commands (#elaborate, etc.)
6. **ResponseFormatter**: Formats output based on content type

### New Dependencies:
```
# OCR and Screenshot
pytesseract
pillow
pyautogui
easyocr  # Alternative OCR

# Content Detection
python-magic  # File type detection
pygments      # Code language detection
```

### New Environment Variables:
- `NO_MORE_TYPO_OCR_ENGINE` (tesseract/easyocr)
- `NO_MORE_TYPO_SCREENSHOT_HOTKEY` (default: ctrl+shift+s)
- `NO_MORE_TYPO_DEBUG` (enable debug logging)

## User Experience Flow

### Scenario 1: Terminal Error Fix
1. User sees error in terminal
2. Takes screenshot (Ctrl+Shift+S)
3. App detects terminal error context
4. LLM provides: `# Fix for [error]: [description]\ncommand_to_fix`
5. User pastes in terminal - gets comment + fix

### Scenario 2: Code Completion
1. User copies incomplete code
2. Presses Ctrl+Shift+Z
3. App detects code context
4. LLM completes/fixes the code
5. User pastes completed code

### Scenario 3: Text with Command
1. User copies text + adds "#explain"
2. Presses Ctrl+Shift+Z
3. App parses command, explains the text
4. User pastes explanation

## Success Metrics
- Accurate content type detection (>90%)
- Appropriate intent recognition (>85%)
- User satisfaction with AI suggestions
- Maintained performance (<2s response time)

## Risk Mitigation
- Fallback to original functionality if detection fails
- Clear error messages for screenshot/OCR issues
- Offline mode for basic typo fixing
- User configuration for enabling/disabling features

---

## Discussion Points
1. **Hotkey Management**: How many hotkeys are too many?
2. **Privacy**: Screenshot data handling and retention
3. **Performance**: OCR processing time impact
4. **Error Handling**: Graceful degradation when components fail
5. **Configuration**: How much customization to expose to users?