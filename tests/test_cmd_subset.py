import pytest
from typer.testing import CliRunner

from tests.conftest import MockedTM1Service
from tm1cli.main import app

runner = CliRunner()


@pytest.mark.parametrize("command", ["list", "ls"])
def test_subset_list(mocker, command):
    mocker.patch("tm1cli.commands.subset.TM1Service", MockedTM1Service)
    result = runner.invoke(app, ["subset", command, "--dimension", "Dimension1"])
    assert result.exit_code == 0
    assert isinstance(result.stdout, str)
    assert "dimension: Dimension1" in result.stdout
    assert "name: Subset1" in result.stdout
    assert "type: public" in result.stdout


def test_subset_exists(mocker):
    mocker.patch("tm1cli.commands.subset.TM1Service", MockedTM1Service)
    result = runner.invoke(app, ["subset", "exists", "Dimension1", "Subset1"])
    assert result.exit_code == 0
    assert isinstance(result.stdout, str)
    assert result.stdout == "True\n"
