import click
from dataclasses import dataclass


@dataclass
class Config:
    connection: str

pass_config = click.make_pass_decorator(Config)

@click.group()
@click.option("-c", "--connection", help="Connection string")
@click.pass_context
def group(ctx: click.Context):
    ctx.obj = Config()


@group.command()
def setup_triggers():
    """Setups the triggers"""
    ...