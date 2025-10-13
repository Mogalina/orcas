import yaml
from pathlib import Path
from typing import Dict, Any

DEFAULT_CONFIG = {
    'model': {
        'name': 'gemma-3',
        'path': str(Path.home() / '.orcas' / 'models'),
        'n_ctx': 2048,
        'n_gpu_layers': 0,
    },
    'security': {
        'require_confirmation': True,
        'allow_sudo': True,
        'blocked_commands': [
            'rm -rf /',
            'dd if=',
            'mkfs',
            ':(){ :|:& };:',
            'chmod -R 777 /',
        ],
        'blocked_patterns': [
            r'rm\s+-rf\s+/',
            r'dd\s+if=/dev/',
        ],
    },
    'execution': {
        'timeout': 300,
        'max_commands_per_request': 10,
        'shell': '/bin/bash',
    },
}


def load_config(config_path: Path = None) -> Dict[str, Any]:
    """Load configuration from file or use defaults."""

    if config_path is None:
        config_path = Path.home() / '.config' / 'orcas' / 'config.yaml'

    if config_path.exists():
        with open(config_path, 'r') as f:
            user_config = yaml.safe_load(f)
            config = DEFAULT_CONFIG.copy()
            config.update(user_config)
            return config

    return DEFAULT_CONFIG


def save_config(config: Dict[str, Any], config_path: Path = None) -> None:
    """Save configuration to file."""

    if config_path is None:
        config_path = Path.home() / '.config' / 'orcas' / 'config.yaml'

    config_path.parent.mkdir(parents=True, exist_ok=True)

    with open(config_path, 'w') as f:
        yaml.dump(config, f, default_flow_style=False)