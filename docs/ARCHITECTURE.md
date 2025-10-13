# Architecture Documentation

## Overview

Orcas is designed with a modular architecture that separates concerns and ensures security at every level.

```
┌─────────────┐
│   CLI       │  User Interface
└──────┬──────┘
       │
┌──────▼──────────────────────┐
│   Command Parser            │  NL → Bash
│   - ModelManager            │
│   - Prompt Engineering      │
└──────┬──────────────────────┘
       │
┌──────▼──────────────────────┐
│   Security Validator        │  Safety Checks
│   - Blocked Commands        │
│   - Pattern Matching        │
│   - Risk Assessment         │
└──────┬──────────────────────┘
       │
┌──────▼──────────────────────┐
│   Command Executor          │  Safe Execution
│   - User Confirmation       │
│   - Sudo Handling           │
│   - Result Display          │
└─────────────────────────────┘
```

## Components

### 1. CLI Layer (`cli.py`)

**Responsibilities:**
- Parse command-line arguments
- Handle interactive mode
- Coordinate other components
- Display results to user

**Key Features:**
- Rich terminal UI with colors
- Interactive prompt
- Dry-run mode support

### 2. Model Manager (`model_manager.py`)

**Responsibilities:**
- Load local LLM models
- Manage model inference
- Handle model caching

**Supported Models:**
- Phi-2 (2.7B) - Recommended
- TinyLlama (1.1B) - Fastest
- Llama 3.2 (1B) - Balanced
- DeepSeek Coder (1.3B) - Code-specialized

**Design Decisions:**
- Uses GGUF format for efficiency
- Lazy loading for faster startup
- Configurable context window

### 3. Command Parser (`command_parser.py`)

**Responsibilities:**
- Convert natural language to bash
- Extract commands from model output
- Validate command structure
- Assess risk levels

**Pipeline:**
1. Build prompt with system instructions
2. Generate response from LLM
3. Extract commands using regex
4. Validate no command chaining
5. Analyze sudo requirements
6. Assess risk level

**Anti-Chaining Logic:**
```python
# Blocked patterns:
- && (AND operator)
- || (OR operator)
- ; (command separator)
- | (pipe - context dependent)
```

### 4. Security Validator (`security.py`)

**Responsibilities:**
- Block dangerous commands
- Detect injection attempts
- Enforce security policies

**Security Layers:**

1. **Blocked Commands List**
   - Hardcoded dangerous commands
   - User-configurable additions

2. **Pattern Matching**
   - Regex-based detection
   - Context-aware analysis

3. **Injection Detection**
   - Command substitution (`$(...)`)
   - Backtick execution
   - Network redirections

4. **Risk Assessment**
   - Low: Read operations
   - Medium: Modify operations
   - High: Delete/format operations

### 5. Command Executor (`executor.py`)

**Responsibilities:**
- Execute validated commands
- Handle user confirmations
- Manage sudo elevation
- Capture and display output

**Execution Flow:**
```
1. Validate command (Security Layer)
2. Display command + risk level
3. Request user confirmation
4. Check sudo requirement
5. Execute with timeout
6. Capture output/errors
7. Display results
```

**Safety Features:**
- Timeout protection (default 300s)
- Subprocess isolation
- Error handling
- Stop-on-failure option

## Configuration System (`config.py`)

**Hierarchy:**
1. Default configuration (built-in)
2. System config (`/etc/orcas/config.yaml`)
3. User config (`~/.config/orcas/config.yaml`)
4. CLI arguments (highest priority)

**Configuration Schema:**
```yaml
model:          # LLM settings
security:       # Security policies
execution:      # Execution behavior
logging:        # Logging configuration
```

## Data Flow

### Single Command Flow

```
User Input
    ↓
CLI Parser
    ↓
Model Manager (NL → Bash)
    ↓
Command Parser (Extract & Analyze)
    ↓
Security Validator (Check Safety)
    ↓
User Confirmation
    ↓
Command Executor (Execute)
    ↓
Result Display
```

### Interactive Mode Flow

```
Start Interactive Loop
    ↓
Read User Input ──┐
    ↓             │
Process Command   │
    ↓             │
Display Result    │
    ↓             │
Check Exit ───────┘
    ↓
Exit
```

## Security Design

### Defense in Depth

1. **Input Validation**
   - Sanitize user input
   - Detect malicious patterns

2. **Command Parsing**
   - No command chaining allowed
   - Strict command extraction

3. **Security Validation**
   - Multiple validation layers
   - Configurable policies

4. **User Confirmation**
   - Interactive approval
   - Risk-based warnings

5. **Execution Isolation**
   - Subprocess execution
   - Timeout protection

### Threat Model

**Protected Against:**
- Command injection
- Privilege escalation
- System damage
- Data loss
- Resource exhaustion

**Not Protected Against:**
- Social engineering (user approves bad command)
- Physical access
- Kernel exploits

## Performance Considerations

### Model Loading
- First load: 2-5 seconds
- Cached: <1 second
- Memory: 2-4GB RAM

### Inference Time
- Simple commands: <1 second
- Complex commands: 1-3 seconds

### Optimizations
- Model quantization (Q4_K_M)
- Lazy loading
- Response caching (future)

## Extensibility

### Adding New Models

```python
# model_manager.py
SUPPORTED_MODELS = {
    "new-model": {
        "url": "...",
        "filename": "...",
    }
}
```

### Custom Security Rules

```yaml
# config.yaml
security:
  custom_validators:
    - "path/to/validator.py"
```

### Plugin System (Future)

```
plugins/
├── validators/
├── parsers/
└── executors/
```

## Testing Strategy

### Unit Tests
- Command parser logic
- Security validation
- Configuration loading

### Integration Tests
- End-to-end command flow
- Model inference
- Execution pipeline

### Security Tests
- Injection attempts
- Blocked command enforcement
- Privilege escalation prevention

## Future Enhancements

1. **Command History**
   - SQLite database
   - Search and replay

2. **Learning Mode**
   - User feedback
   - Model fine-tuning

3. **Alias System**
   - Save common commands
   - Custom shortcuts

4. **Multi-Model Support**
   - Ensemble predictions
   - Fallback models

5. **Web UI**
   - Browser interface
   - Command history viewer
```
