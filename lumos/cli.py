import subprocess
import sys

import click
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.text import Text
from lumos.engine import suggest, explain
from lumos.history import save_entry, get_recent

console = Console()

def _display_command(command):
    text = Text()
    text.append("$ ", style="green bold")
    text.append(command)
    console.print(
        Panel(text, title="lumos", title_align="left", border_style="blue", padding=(1, 2))
    )

def _history(limit):
    entries = get_recent(limit)
    if not entries:
        console.print("  no history yet", style="dim")
        return
    table = Table(title="history", border_style="blue", show_header=True, header_style="bold")
    table.add_column("time", style="dim")
    table.add_column("description")
    table.add_column("command", style="green")
    for entry in entries:
        ts = entry["timestamp"][:16].replace("T", " ")
        table.add_row(ts, entry["description"], entry["command"])
    console.print(table)

@click.command()
@click.argument("input_text", required=False)
@click.option("-e", "--explain", "explain_mode", is_flag=True)
@click.option("-H", "--history", "show_history", is_flag=True)
@click.option("-n", "--limit", default=20)
def cli(input_text, explain_mode, show_history, limit):
    if show_history:
        _history(limit)
    elif explain_mode:
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
            save_entry(input_text, command)
            console.print()
            result = subprocess.run(command, shell=True)
            sys.exit(result.returncode)
        else:
            save_entry(input_text, command)
    else:
        click.echo(click.get_current_context().get_help())
