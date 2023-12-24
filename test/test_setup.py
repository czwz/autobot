import pytest

from click.testing import CliRunner

from src.setup import hello


SOMETHING_TO_SHOUT: str = "test"


@pytest.mark.setup
def test_hello_with_shout() -> None:
    runner = CliRunner()
    result = runner.invoke(hello, ['--shout', SOMETHING_TO_SHOUT])
    assert result.exit_code == 0
    assert SOMETHING_TO_SHOUT in result.output

@pytest.mark.setup
def test_hello_without_shout() -> None:
    runner = CliRunner()
    result = runner.invoke(hello)
    assert result.exit_code == 0
    assert "Hello, World!" in result.output
