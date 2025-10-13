import click
import sys
from pathlib import Path
from typing import Optional
from rich.console import Console
from rich.panel import Panel

from config import load_config
from model_manager import ModelManager
from command_parser import CommandParser
from executor import CommandExecutor
from security import SecurityValidator

console = Console()


@click.command()
@click.argument('prompt', nargs=-1, required=False)
@click.option('--interactive', '-i', is_flag=True, help='Start interactive mode')
@click.option('--dry-run', '-d', is_flag=True, help='Show commands without executing')
@click.option('--config', '-c', type=click.Path(), help='Path to config file')
@click.option('--download-model', is_flag=True, help='Download default model')
@click.option('--version', is_flag=True, help='Show version')
def main(
        prompt: tuple,
        interactive: bool,
        dry_run: bool,
        config: Optional[str],
        download_model: bool,
        version: bool
) -> None:
    """Orcas - Transform natural language into bash commands."""

    if version:
        console.print("🐋 Orcas v0.1.0")
        return

    if download_model:
        import subprocess
        subprocess.run([sys.executable, "scripts/download_model.py"])
        return

    config_path = Path(config) if config else None
    cfg = load_config(config_path)

    try:
        model_manager = ModelManager(cfg['model'])
        command_parser = CommandParser(model_manager)
        security_validator = SecurityValidator(cfg['security'])
        executor = CommandExecutor(cfg['execution'], security_validator)
    except Exception as e:
        console.print(f"✗ Initialization failed: {e}", style="red")
        sys.exit(1)

    if interactive:
        run_interactive_mode(command_parser, executor, dry_run)
        return

    if not prompt:
        console.print("Error: Please provide a command or use --interactive", style="red")
        console.print("\nUsage: orcas <prompt> | --interactive")
        sys.exit(1)

    user_input = ' '.join(prompt)
    process_command(user_input, command_parser, executor, dry_run)


def process_command(
        user_input: str,
        parser: CommandParser,
        executor: CommandExecutor,
        dry_run: bool
) -> None:
    """Process a single natural language command."""

    try:
        # Parse natural language to commands
        commands = parser.parse(user_input)
        if not commands:
            console.print("✗ Could not generate valid commands", style="red")
            return

        # Display commands
        console.print(f"Generated {len(commands)} command(s):")
        for i, cmd in enumerate(commands, 1):
            style = "yellow" if cmd.requires_sudo else "green"
            sudo_prefix = "[red]sudo[/red] " if cmd.requires_sudo else ""
            console.print(f"  {i}. {sudo_prefix}[{style}]{cmd.command}[/{style}]")

        if dry_run:
            console.print("\n[yellow]Dry run - no commands executed[/yellow]")
            return

        # Execute commands
        executor.execute_commands(commands)

    except KeyboardInterrupt:
        console.print("\n\n✗ Cancelled by user", style="yellow")
    except Exception as e:
        console.print(f"\n✗ Error: {e}", style="red")


def run_interactive_mode(
        parser: CommandParser,
        executor: CommandExecutor,
        dry_run: bool
) -> None:
    """Run Orcas in interactive mode."""

    console.print(Panel.fit(
        "[cyan]Orcas Interactive Mode[/cyan]\n"
        "Type your commands in natural language\n"
        "Type 'exit' or 'quit' to leave",
        border_style="cyan"
    ))

    while True:
        try:
            user_input = console.input("\n[green]orcas>[/green] ").strip()

            if not user_input:
                continue

            if user_input.lower() in ('exit', 'quit', 'q'):
                console.print("Goodbye!", style="cyan")
                break

            process_command(user_input, parser, executor, dry_run)

        except KeyboardInterrupt:
            console.print("\nGoodbye!", style="cyan")
            break
        except EOFError:
            break


if __name__ == '__main__':
    main()