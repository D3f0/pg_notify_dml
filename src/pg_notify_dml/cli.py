# noqa: T201, RUF100
from dataclasses import dataclass, field

import click

# from sqlalchemy import DDL
from sqlalchemy import Engine, MetaData, create_engine


@dataclass
class Config:
    connection: str
    engine: Engine = field(init=False, default=None)
    metadata: MetaData = field(init=False, default=None, repr=False)

    def __post_init__(self):
        if self.connection:
            self.engine = create_engine(self.connection)
            if self.engine.driver not in {"psycopg", "psycopg2"}:
                msg = "This tool only support Postgres databases"
                raise ValueError(msg)
            self.metadata = MetaData()
            self.metadata.reflect(self.engine)


pass_config = click.make_pass_decorator(Config)


@click.group()
@click.option("-c", "--connection", help="Connection string")
@click.pass_context
def group(ctx: click.Context, connection: str):
    ctx.obj = Config(
        connection=connection,
    )


@group.command()
@pass_config
def show_tables(config: Config):
    """Shows available tables in the connection"""
    if not config.metadata:
        message = "A connection is required"
        raise click.UsageError(message)
    tables = "\n".join(config.metadata.tables.keys())
    click.secho(tables)


@group.command()
@pass_config
def setup_trigger(config: Config):
    """Setups the trigger"""
    if not config.engine:
        message = "Can't operate without a connection"
        raise click.UsageError(message)
