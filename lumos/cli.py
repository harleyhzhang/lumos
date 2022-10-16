import click
from lumos.engine import suggest

@click.command()
@click.argument("description")
def cli(description):
    command = suggest(description)
    click.echo(command)
