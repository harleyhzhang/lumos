import subprocess
import sys

import click
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from lumos.engine import suggest, explain

console = Console()

def _display_command(command):
    text = Text()
    text.append("$ ", style="green bold")
    text.append(command)
    console.print(
        Panel(text, title="lumos", title_align="left", border_style="blue", padding=(1, 2))
    )

@click.command()
@click.argument("input_text", required=False)
@click.option("-e", "--explain", "explain_mode", is_flag=True)
def cli(input_text, explain_mode):
    if explain_mode:
        if not input_text:
            console.print("  provide a command to explain", style="red")
            raise SystemExit(1)
        with console.status("thinking...", spinner="dots"):
            explanation = explain(input_text)
        text = Text()
        text.append("$ ", style="green bold")
        text.append(input_text)
        text.append("\n\n")
        text.append(explanation, style="dim")
        console.print(
            Panel(text, title="lumos", title_align="left", border_style="blue", padding=(1, 2))
        )
    elif input_text:
        with console.status("thinking...", spinner="dots"):
            command = suggest(input_text)
        _display_command(command)
        should_run = console.input(
            "\n  run this command? [dim]\\[y/n][/dim] "
        ).strip().lower() == "y"
        if should_run:
            console.print()
            result = subprocess.run(command, shell=True)
            sys.exit(result.returncode)
    else:
        click.echo(click.get_current_context().get_help())
