import sqlalchemy
from click.testing import CliRunner
from sqlalchemy.orm import declarative_base
from testcontainers import postgres

from pg_notify_dml.cli import group


def test_testcontainer_db_connects_to_sa():
    with postgres.PostgresContainer() as db:
        url = db.get_connection_url()
        sqlalchemy.create_engine(url)


def test_show_tables():
    Base = declarative_base()
    table_name = "test_table"
    class TestTable(Base):
        __tablename__ = table_name
        id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
        name = sqlalchemy.Column(sqlalchemy.String)

    with postgres.PostgresContainer() as db:
        url = db.get_connection_url()
        engine = sqlalchemy.create_engine(url)
        Base.metadata.create_all(engine)
        runner = CliRunner()
        result = runner.invoke(group, ["-c", url, "show-tables"])
        assert result.exit_code == 0
        assert table_name in result.output


def test_create_trigger():
    Base = declarative_base()
    table_name = "test_table"
    class TestTable(Base):
        __tablename__ = table_name
        id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
        name = sqlalchemy.Column(sqlalchemy.String)

    with postgres.PostgresContainer() as db:
        url = db.get_connection_url()
        engine = sqlalchemy.create_engine(url)
        Base.metadata.create_all(engine)
        runner = CliRunner()
        result = runner.invoke(group, ["-c", url, "show-tables"])
        assert result.exit_code == 0
        assert table_name in result.output