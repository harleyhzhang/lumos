import click
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from lumos.engine import suggest

console = Console()

@click.command()
@click.argument("description")
def cli(description):
    command = suggest(description)
    text = Text()
    text.append("$ ", style="green bold")
    text.append(command)
    console.print(
        Panel(text, title="lumos", title_align="left", border_style="blue", padding=(1, 2))
    )
    should_run = console.input(
        "\n  run this command? [dim]\\[y/n][/dim] "
    ).strip().lower() == "y"
