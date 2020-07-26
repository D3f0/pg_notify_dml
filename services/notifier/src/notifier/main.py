import typer
from loguru import logger
import asyncio
import asyncpg
import rich

app = typer.Typer()


@app.command()
def main(name: str):
    typer.echo(name)


@app.command()
@logger.catch()
def show_events(
    user: str = typer.Option(
        expose_value=True, show_default=True, envvar="DB_USER", default="postgres"
    ),
    password: str = typer.Option(envvar="DB_PASSWORD", default="postgres"),
    name: str = typer.Option(envvar="DB_NAME", default="example"),
    host: str = typer.Option(envvar="DB_HOST", default="postgres"),
    port: int = typer.Option(envvar="DB_PORT", default=5432),
    channel: str = typer.Option(envvar="DB_CHANNEL", default="events"),
):
    def callback(connection, pid, channel, payload) -> None:
        rich.print(locals())

    async def run():
        conn: asyncpg.connection.Connection = await asyncpg.connect(
            user=user, password=password, database=name, host=host, port=port,
        )
        await conn.add_listener(channel, callback)
        while True:
            await asyncio.sleep(.1)

    loop = asyncio.get_event_loop()
    loop.run_until_complete(run())


if __name__ == "__main__":
    app()

