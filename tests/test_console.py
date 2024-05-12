"""Test console."""

import click.testing
import pytest
import requests

from iitp_6_python import console
from unittest.mock import Mock
from pytest_mock import MockFixture
from click.testing import CliRunner


@pytest.fixture
def mock_requests_get(mocker: MockFixture) -> Mock:
    """Fixture for mocking requests.get function.

    Args:
        mocker(MockFixture): mocking object.

    Returns:
        Mock: A patched version of requests.get.
    """
    mock = mocker.patch("requests.get")
    mock.return_value.__enter__.return_value.json.return_value = {
        "title": "Lorem Ipsum",
        "extract": "Lorem ipsum dolor sit amet",
    }
    return mock


@pytest.fixture
def runner() -> CliRunner:
    """Fixture for CliRunner.

    Returns:
        CliRunner: An instance of CliRunner.
    """
    return click.testing.CliRunner()


@pytest.fixture
def mock_wikipedia_random_page(mocker: MockFixture) -> Mock:
    """Fixture for mocking wikipedia.random_page function.

    Args:
        mocker(MockFixture): mocking object.

    Returns:
        Mock: A patched version of wikipedia.random_page.
    """
    return mocker.patch("iitp_6_python.wikipedia.random_page")


@pytest.mark.e2e
def test_main_succeeds_in_production_env(runner: CliRunner) -> None:
    """Test if the main function succeeds in production environment.

    Args:
        runner (CliRunner): An instance of CliRunner.
    """
    result = runner.invoke(console.main)
    assert result.exit_code == 0


def test_main_uses_specified_language(
    runner: CliRunner, mock_wikipedia_random_page: Mock
) -> None:
    """Test if the main function uses the specified language.

    Args:
        runner (CliRunner): An instance of CliRunner.
        mock_wikipedia_random_page (Mock): A mocked version of wikipedia.random_page.
    """
    runner.invoke(console.main, ["--language=pl"])
    mock_wikipedia_random_page.assert_called_with(language="pl")


def test_main_succeeds(runner: CliRunner, mock_requests_get: Mock) -> None:
    """Test if the main function succeeds.

    Args:
        runner (CliRunner): An instance of CliRunner.
        mock_requests_get (Mock): A mocked version of requests.get.
    """
    result = runner.invoke(console.main)
    assert result.exit_code == 0


def test_main_prints_title(runner: CliRunner, mock_requests_get: Mock) -> None:
    """Test if the main function prints the title.

    Args:
        runner (CliRunner): An instance of CliRunner.
        mock_requests_get (Mock): A mocked version of requests.get.
    """
    result = runner.invoke(console.main)
    assert "Lorem Ipsum" in result.output


def test_main_invokes_requests_get(runner: CliRunner, mock_requests_get: Mock) -> None:
    """Test if the main function invokes requests.get.

    Args:
        runner (CliRunner): An instance of CliRunner.
        mock_requests_get (Mock): A mocked version of requests.get.
    """
    runner.invoke(console.main)
    assert mock_requests_get.called


def test_main_uses_en_wikipedia_org(runner: CliRunner, mock_requests_get: Mock) -> None:
    """Test if the main function uses en.wikipedia.org.

    Args:
        runner (CliRunner): An instance of CliRunner.
        mock_requests_get (Mock): A mocked version of requests.get.
    """
    runner.invoke(console.main)
    args, _ = mock_requests_get.call_args
    assert "en.wikipedia.org" in args[0]


def test_main_fails_on_request_error(
    runner: CliRunner, mock_requests_get: Mock
) -> None:
    """Test if the main function fails on request error.

    Args:
        runner (CliRunner): An instance of CliRunner.
        mock_requests_get (Mock): A mocked version of requests.get.
    """
    mock_requests_get.side_effect = Exception("Boom")
    result = runner.invoke(console.main)
    assert result.exit_code == 1


def test_main_prints_message_on_request_error(
    runner: CliRunner, mock_requests_get: Mock
) -> None:
    """Test if the main function prints a message on request error.

    Args:
        runner (CliRunner): An instance of CliRunner.
        mock_requests_get (Mock): A mocked version of requests.get.
    """
    mock_requests_get.side_effect = requests.RequestException
    result = runner.invoke(console.main)
    assert "Error" in result.output
