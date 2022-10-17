import subprocess
import sys

import click
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from lumos.engine import suggest

console = Console()

def _display_command(command):
    text = Text()
    text.append("$ ", style="green bold")
    text.append(command)
    console.print(
        Panel(text, title="lumos", title_align="left", border_style="blue", padding=(1, 2))
    )

@click.command()
@click.argument("description")
def cli(description):
    with console.status("thinking...", spinner="dots"):
        command = suggest(description)
    _display_command(command)
    should_run = console.input(
        "\n  run this command? [dim]\\[y/n][/dim] "
    ).strip().lower() == "y"
    if should_run:
        console.print()
        result = subprocess.run(command, shell=True)
        sys.exit(result.returncode)
