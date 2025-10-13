# Orcas

Transform natural language into safe, executable bash commands using local AI models.

## Features

- Local AI model execution with no cloud dependencies
- Security-first design with command validation
- No command chaining to prevent dangerous operations
- Interactive approval for multistep commands
- Smart sudo privilege handling

## Installation

```bash
git clone https://github.com/Mogalina/orcas.git
cd orcas
./scripts/install.sh
```

## Usage

```bash
# Single command mode
orcas find all python files larger than 1MB
orcas create backup of documents folder
orcas show disk usage sorted by size

# Interactive mode
orcas --interactive

# Preview commands without executing
orcas --dry-run compress logs folder
```

## Configuration

Configuration file: `~/.config/orcas/config.yaml`

```yaml
model:
  name: "gemma-3"
  path: "~/.orcas/models"
  
security:
  require_confirmation: true
  allow_sudo: true
  
execution:
  timeout: 300
```

## Supported Models

|   Model   | Parameters (B) | Size (GB) |
|:---------:|:--------------:|:---------:|
|  Gemma3   |      12.2      |    7.3    |
|   Phi-2   |      2.7       |    1.2    |
| TinyLlama |      1.1       |    0.7    |

## Security

- Command validation before execution
- No automatic command chaining
- Sudo privilege confirmation
- Dangerous command blacklist
- Command preview before execution

## Documentation

- [Installation Guide](docs/INSTALLATION.md)
- [Usage Guide](docs/USAGE.md)
- [Architecture](docs/ARCHITECTURE.md)

## Requirements

- Python 3.8 or higher
- 4GB RAM minimum
- 8GB disk space for models

## License

[MIT License](LICENSE)