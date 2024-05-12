"""Configure pytest."""

import pytest
from unittest.mock import Mock

from pytest_mock import MockFixture
from _pytest.config import Config


@pytest.fixture
def mock_requests_get(mocker: MockFixture) -> Mock:
    """Fixture for mocking requests.get function.

    Args:
        mocker (MockFixture): A fixture provided by pytest_mock.

    Returns:
        Mock: A patched version of requests.get.
    """
    mock = mocker.patch("requests.get")
    mock.return_value.__enter__.return_value.json.return_value = {
        "title": "Lorem Ipsum",
        "extract": "Lorem ipsum dolor sit amet",
    }
    return mock


def pytest_configure(config: Config) -> None:
    """Configure pytest markers.

    Args:
        config (Config): The pytest config object.
    """
    config.addinivalue_line("markers", "e2e: mark as end-to-end test.")
