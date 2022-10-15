import click

@click.command()
@click.argument("description")
def cli(description):
    click.echo(f"TODO: {description}")
