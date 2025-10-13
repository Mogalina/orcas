import re
from dataclasses import dataclass
from typing import List, Optional
from model_manager import ModelManager


@dataclass
class Command:
    """Represents a parsed bash command."""
    command: str
    description: str
    requires_sudo: bool = False
    risk_level: str = "low"


class CommandParser:
    """Parses natural language into bash commands using LLM."""

    SYSTEM_PROMPT = """You are a bash command generator. Convert natural language requests into safe, single bash commands.

CRITICAL RULES:
1. Generate ONLY ONE command per line
2. NEVER use command chaining (&&, ||, ;, |)
3. If multiple steps needed, output each on a new line
4. Each command must be complete and standalone
5. Use full paths when possible
6. Output format: actual_command

Examples:
User: find large python files
find . -name "*.py" -size +1M

User: create backup and compress it
cp -r documents documents_backup
tar -czf documents_backup.tar.gz documents_backup

User: list files sorted by size
ls -lhS"""

    def __init__(self, model_manager: ModelManager):
        self.model = model_manager

    def parse(self, natural_language: str) -> List[Command]:
        """Parse natural language into bash commands."""

        # Create prompt
        prompt = f"{self.SYSTEM_PROMPT}\n\nUser: {natural_language}\n"

        # Generate commands
        response = self.model.generate(prompt, max_tokens=512)

        # Extract commands
        commands = self._extract_commands(response)

        # Analyze each command
        parsed_commands = []
        for cmd_str in commands:
            cmd = self._analyze_command(cmd_str, natural_language)
            if cmd:
                parsed_commands.append(cmd)

        return parsed_commands

    def _extract_commands(self, response: str) -> List[str]:
        """Extract command strings from model output."""
        commands = []

        xml_pattern = r"<command>(.*?)</command>"
        xml_matches = re.findall(xml_pattern, response, re.DOTALL | re.IGNORECASE)
        if xml_matches:
            commands.extend([cmd.strip() for cmd in xml_matches if cmd.strip()])
        else:
            lines = response.split('\n')
            for line in lines:
                line = line.strip()
                if line and not line.startswith('#') and not line.startswith('//'):
                    # Remove common prefixes
                    line = re.sub(r'^(Command:|Bash:|Shell:|\$)\s*', '', line)
                    if line:
                        commands.append(line)

        # Validate commands don't contain chaining
        valid_commands = []
        for cmd in commands:
            if self._validate_no_chaining(cmd):
                valid_commands.append(cmd)

        return valid_commands

    def _validate_no_chaining(self, command: str) -> bool:
        """Ensure command doesn't use chaining operators."""
        # Check for command chaining
        chaining_patterns = [
            r'&&',
            r'\|\|',
            r';\s*\w',
        ]

        for pattern in chaining_patterns:
            if re.search(pattern, command):
                return False

        return True

    def _analyze_command(self, command: str, context: str) -> Optional[Command]:
        """Analyze command for safety and requirements."""
        # Check if sudo is needed
        requires_sudo = self._check_sudo_needed(command)

        # Determine risk level
        risk_level = self._assess_risk(command)

        # Generate description
        description = self._generate_description(command, context)

        return Command(
            command=command,
            description=description,
            requires_sudo=requires_sudo,
            risk_level=risk_level
        )

    def _check_sudo_needed(self, command: str) -> bool:
        """Check if command requires sudo privileges."""
        sudo_indicators = [
            'apt', 'yum', 'dnf', 'pacman',
            'systemctl', 'service',
            'mount', 'umount',
            'useradd', 'userdel', 'usermod',
            'chown', 'chmod',
        ]

        cmd_parts = command.split()
        if not cmd_parts:
            return False

        base_cmd = cmd_parts[0]

        # Already has sudo
        if base_cmd == 'sudo':
            return True

        # Check if command typically needs sudo
        for indicator in sudo_indicators:
            if indicator in command:
                return True

        # Check if writing to system directories
        system_dirs = ['/etc/', '/usr/', '/var/', '/sys/', '/proc/']
        for dir_path in system_dirs:
            if dir_path in command and ('>' in command or 'cp' in command or 'mv' in command):
                return True

        return False

    def _assess_risk(self, command: str) -> str:
        """Assess the risk level of a command."""
        high_risk_patterns = [
            r'\brm\b.*-[rf]',
            r'\bdd\b',
            r'\bmkfs\b',
            r'\bformat\b',
            r'>\s*/dev/',
        ]

        medium_risk_patterns = [
            r'\brm\b',
            r'\bmv\b.*/',
            r'\bchmod\b',
            r'\bchown\b',
        ]

        for pattern in high_risk_patterns:
            if re.search(pattern, command):
                return 'high'

        for pattern in medium_risk_patterns:
            if re.search(pattern, command):
                return 'medium'

        return 'low'

    def _generate_description(self, command: str, context: str) -> str:
        """Generate a human-readable description of the command."""
        return f"Execute: {command}"