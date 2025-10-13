import re
from command_parser import Command


class SecurityValidator:
    """Validates commands for security concerns."""

    def __init__(self, config: dict):
        self.config = config
        self.blocked_commands = config.get('blocked_commands', [])
        self.blocked_patterns = [
            re.compile(pattern)
            for pattern in config.get('blocked_patterns', [])
        ]

    def validate(self, command: Command) -> bool:
        """Validate a command for security."""

        # Check blocked commands
        if self._is_blocked_command(command.command):
            return False

        # Check blocked patterns
        if self._matches_blocked_pattern(command.command):
            return False

        # Check for command injection attempts
        if self._has_injection_attempt(command.command):
            return False

        # Check high-risk commands
        if command.risk_level == 'high':
            if not self.config.get('allow_high_risk', False):
                return False

        return True

    def _is_blocked_command(self, command: str) -> bool:
        """Check if command is in blocked list."""
        for blocked in self.blocked_commands:
            if blocked in command:
                return True
        return False

    def _matches_blocked_pattern(self, command: str) -> bool:
        """Check if command matches blocked patterns."""
        for pattern in self.blocked_patterns:
            if pattern.search(command):
                return True
        return False

    def _has_injection_attempt(self, command: str) -> bool:
        """Detect potential command injection attempts."""
        injection_indicators = [
            r'\$\(.*\)',       # Command substitution
            r'`.*`',           # Backtick substitution
            r'>\s*/dev/tcp/',  # Network redirection
            r'curl.*\|.*sh',   # Piping to shell
            r'wget.*\|.*sh',   # Piping to shell
        ]

        for indicator in injection_indicators:
            if re.search(indicator, command):
                return True

        return False