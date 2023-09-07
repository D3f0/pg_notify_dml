# noqa: T201, RUF100
from functools import lru_cache
import click
from dataclasses import dataclass, field
from sqlalchemy import create_engine, Engine, MetaData, DDL

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
    if config.metadata:
        print(*config.metadata.tables.keys(), sep="\n")
    else:
        print("A connection is required.")  # noqa: T201, RUF100

@group.command()
@pass_config
def setup_trigger(config: Config):
    """Setups the trigger"""
    if not config.engine:
        print("Can't operate without a connection") # noqa: RUF100
    else:
        breakpoint()
        
