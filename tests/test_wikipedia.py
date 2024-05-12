"""Wikipedia tests."""

import click
from iitp_6_python import wikipedia

from unittest.mock import Mock
import pytest


def test_random_page_returns_page(mock_requests_get: Mock) -> None:
    """Test if random_page function returns a Page object.

    Args:
        mock_requests_get (Mock): A mocked version of requests.get.
    """
    page = wikipedia.random_page()
    assert isinstance(page, wikipedia.Page)


def test_random_page_handles_validation_errors(mock_requests_get: Mock) -> None:
    """Test if random_page function handles validation errors properly.

    Args:
        mock_requests_get (Mock): A mocked version of requests.get.
    """
    mock_requests_get.return_value.__enter__.return_value.json.return_value = None
    with pytest.raises(click.ClickException):
        wikipedia.random_page()


# def test_trigger_typeguard(mock_requests_get):
#     """Test trigger for typeguard.

#     Args:
#         mock_requests_get: Mock object for requests.get
#     """
#     import json

#     data = json.loads('{ "language": 1 }')
#     wikipedia.random_page(language=data["language"])
