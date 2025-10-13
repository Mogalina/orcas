# Usage Guide

## Basic Usage

### Single Command Mode

```bash
orcas [your natural language command]
```

Examples:
```bash
orcas find all python files larger than 1MB
orcas create a backup of my documents folder
orcas show disk usage sorted by size
orcas count lines in all javascript files
```

### Interactive Mode

```bash
orcas --interactive
```

In interactive mode, you can enter multiple commands:
```
orcas> find large log files
orcas> compress them into archive
orcas> exit
```

### Dry Run Mode

Preview commands without executing:
```bash
orcas --dry-run create backup of photos
```

## Command Examples

### File Operations

```bash
# Find files
orcas find all pdf files modified in last 7 days
orcas locate files larger than 100MB

# Copy/Move
orcas copy all images to backup folder
orcas move old logs to archive directory

# Compression
orcas compress documents folder into tar.gz
orcas extract backup.zip to current directory
```

### System Information

```bash
orcas show disk usage
orcas display memory usage
orcas list running processes sorted by memory
orcas check system uptime
```

### Text Processing

```bash
orcas count lines in all python files
orcas find TODO comments in source code
orcas search for error in log files from today
```

### Network Operations

```bash
orcas check if port 8080 is open
orcas show active network connections
orcas ping google.com 5 times
```

## Options

### Global Options

- `--interactive, -i`: Start interactive mode
- `--dry-run, -d`: Show commands without executing
- `--config PATH`: Use custom config file
- `--version`: Show version
- `--help`: Show help message

### Configuration

Edit `~/.config/orcas/config.yaml`:

```yaml
# Require confirmation before execution
security:
  require_confirmation: true  # false for auto-execute

# Allow sudo commands
security:
  allow_sudo: true

# Execution timeout
execution:
  timeout: 300  # seconds
```

## Multi-Step Commands

Orcas breaks complex requests into multiple commands:

```bash
orcas create a folder called backup, copy all photos to it, then compress it
```

Output:
```
Generated 3 commands:
1. mkdir backup
2. cp -r photos/* backup/
3. tar -czf backup.tar.gz backup

Execute command 1? [Y/n]
Execute command 2? [Y/n]
Execute command 3? [Y/n]
```

## Security Features

### Confirmation Prompts

All commands require confirmation (unless disabled):
```
Command: rm old_file.txt
Risk level: MEDIUM
Execute this command? [Y/n]
```

### Sudo Handling

Commands requiring privileges prompt twice:
```
Command: apt install vim
This command requires sudo. Proceed? [y/N]
```

### Blocked Commands

Dangerous commands are automatically blocked:
- `rm -rf /`
- `dd if=/dev/zero`
- Fork bombs
- System-wide permission changes

## Tips & Best Practices

1. **Be Specific**: More detailed prompts lead to better commands
   - Bad: "find files"
   - Good: "find python files modified in last week larger than 1MB"

2. **Review Before Executing**: Always check generated commands

3. **Use Dry Run**: Test complex operations first
   ```bash
   orcas --dry-run delete all temp files
   ```

4. **Interactive for Multiple Operations**: Use interactive mode for workflows

5. **Check Logs**: Review `~/.orcas/logs/orcas.log` for history

## Common Issues

### Command Not Found

```bash
source .venv/bin/activate
# or
export PATH="$PATH:$HOME/.local/bin"
```

### Model Loading Slow

First load takes time. Subsequent uses are faster.

### Commands Not Working

Try being more specific:
```bash
# Instead of:
orcas backup photos

# Try:
orcas create tar.gz archive of photos directory
```

## Advanced Usage

### Custom Model

```yaml
# ~/.config/orcas/config.yaml
model:
  name: "custom-model"
  path: "/path/to/models"
```

### Disable Confirmation

```yaml
security:
  require_confirmation: false
```

**Warning**: Only for trusted environments!

### Custom Blocked Commands

```yaml
security:
  blocked_commands:
    - "your-dangerous-command"
  blocked_patterns:
    - 'regex-pattern'
```