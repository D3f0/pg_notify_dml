import pytest
from click.testing import CliRunner

from pg_notify_dml import cli


def test_cli():
    runner = CliRunner()
    result = runner.invoke(cli.group, [])
    assert result.exit_code == 0
