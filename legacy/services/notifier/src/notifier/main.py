import asyncio
from dataclasses import dataclass
from typing import List, Optional

import asyncpg
import rich
import typer
from asyncpg import Record
from asyncpg.connection import Connection
from loguru import logger
from rich.console import Console
from rich.table import Column, Table

app = typer.Typer()


def show_results_as_table(results: List[Record]) -> None:
    """Formats results of queries"""
    first, *_ = results
    table = Table()
    for column in first.keys():
        table.add_column(column)
    for row in results:
        table.add_row(*map(str, row))
    console = Console()
    console.print(table)


@dataclass
class Config:
    name: Optional[str] = None
    user: Optional[str] = None
    password: Optional[str] = None
    host: Optional[str] = None
    port: Optional[int] = None

    async def get_conn(self) -> Connection:
        return await asyncpg.connect(
            host=self.host,
            port=self.port,
            database=self.name,
            user=self.user,
            password=self.password,
        )


config: Config = Config()


@app.callback()
def main(
    user: str = typer.Option(
        expose_value=True, show_default=True, envvar="DB_USER", default="postgres"
    ),
    password: str = typer.Option(envvar="DB_PASSWORD", default="postgres"),
    name: str = typer.Option(envvar="DB_NAME", default="example"),
    host: str = typer.Option(envvar="DB_HOST", default="postgres"),
    port: int = typer.Option(envvar="DB_PORT", default=5432),
):
    config.user = user
    config.password = password
    config.name = name
    config.host = host
    config.port = port


@app.command()
def show_tables():
    async def fetch_tables():
        conn: Connection = await config.get_conn()
        sql = "SELECT * FROM pg_catalog.pg_tables WHERE schemaname='public';"
        results = await conn.fetch(sql)
        show_results_as_table(results)

    loop = asyncio.get_event_loop()
    loop.run_until_complete(fetch_tables())


@app.command()
def describe_table(table_name: str):
    async def fetch_tables():
        conn: Connection = await config.get_conn()

        sql = (
            "SELECT "
            "table_name, column_name, data_type "
            "FROM "
            "information_schema.columns "
            "WHERE table_name='{table_name}';"
        ).format(table_name=table_name)
        results = await conn.fetch(sql)
        if not results:
            raise typer.BadParameter(f"{table_name} couldn't be found")
        show_results_as_table(results)

    loop = asyncio.get_event_loop()
    loop.run_until_complete(fetch_tables())


@app.command()
@logger.catch()
def show_events(channel: str = typer.Option(envvar="DB_CHANNEL", default="events"),):
    def callback(connection, pid, channel, payload) -> None:
        rich.print(locals())

    async def run():
        conn = await config.get_conn()
        await conn.add_listener(channel, callback)
        while True:
            await asyncio.sleep(0.1)

    loop = asyncio.get_event_loop()
    loop.run_until_complete(run())


if __name__ == "__main__":
    app()

