import subprocess
from typing import List
from dataclasses import dataclass
from rich.console import Console
from rich.prompt import Confirm

from command_parser import Command
from security import SecurityValidator


@dataclass
class ExecutionResult:
    """Result of command execution."""
    success: bool
    stdout: str
    stderr: str
    return_code: int


class CommandExecutor:
    """Safely executes bash commands with user confirmation."""

    def __init__(self, config: dict, security_validator: SecurityValidator):
        self.config = config
        self.security = security_validator
        self.console = Console()

    def execute_commands(self, commands: List[Command]) -> List[
        ExecutionResult]:
        """Execute a list of commands with user approval."""
        results = []

        for i, cmd in enumerate(commands, 1):
            self.console.print(f"\n[cyan]Command {i}/{len(commands)}:[/cyan]")

            # Security validation
            if not self.security.validate(cmd):
                self.console.print(
                    f"[red]✗ Command blocked by security policy[/red]")
                continue

            # Get user confirmation
            if not self._confirm_execution(cmd):
                self.console.print("[yellow]⊘ Skipped[/yellow]")
                continue

            # Handle sudo if needed
            command_str = cmd.command
            if cmd.requires_sudo and not command_str.startswith('sudo'):
                if self.config.get('allow_sudo', True):
                    if Confirm.ask(
                            "  [yellow]This command requires sudo. Proceed?[/yellow]"):
                        command_str = f"sudo {command_str}"
                    else:
                        self.console.print(
                            "[yellow]⊘ Skipped (sudo required)[/yellow]")
                        continue
                else:
                    self.console.print(
                        "[red]✗ Sudo not allowed by configuration[/red]")
                    continue

            # Execute
            result = self._execute_single(command_str)
            results.append(result)

            # Display result
            self._display_result(result)

            # Stop on failure if configured
            if not result.success and self.config.get('stop_on_error', False):
                self.console.print("[red]⊘ Stopping due to error[/red]")
                break

        return results

    def _confirm_execution(self, cmd: Command) -> bool:
        """Ask user to confirm command execution."""
        if not self.config.get('require_confirmation', True):
            return True

        risk_color = {
            'low': 'green',
            'medium': 'yellow',
            'high': 'red'
        }.get(cmd.risk_level, 'white')

        self.console.print(f"  Risk level: [{risk_color}]{cmd.risk_level.upper()}[/{risk_color}]")

        return Confirm.ask("  Execute this command?", default=True)

    def _execute_single(self, command: str) -> ExecutionResult:
        """Execute a single command."""
        try:
            process = subprocess.run(
                command,
                shell=True,
                capture_output=True,
                text=True,
                timeout=self.config.get('timeout', 300),
                executable=self.config.get('shell', '/bin/bash')
            )

            return ExecutionResult(
                success=process.returncode == 0,
                stdout=process.stdout,
                stderr=process.stderr,
                return_code=process.returncode
            )

        except subprocess.TimeoutExpired:
            return ExecutionResult(
                success=False,
                stdout="",
                stderr="Command timed out",
                return_code=-1
            )
        except Exception as e:
            return ExecutionResult(
                success=False,
                stdout="",
                stderr=str(e),
                return_code=-1
            )

    def _display_result(self, result: ExecutionResult) -> None:
        """Display execution result to user."""
        if result.success:
            if result.stdout:
                self.console.print("\n" + result.stdout)
        else:
            self.console.print(f"[red]✗ Failed (exit code: {result.return_code})[/red]")
            if result.stderr:
                self.console.print(f"[red]{result.stderr}[/red]")