"""
Pytest configuration file for shared fixtures and configuration.

This file is automatically loaded by pytest and can contain shared fixtures,
hooks, and configuration used across all test modules.
"""

import pytest
import requests
from typing import Generator


@pytest.fixture(scope="module")
def api_session() -> Generator[requests.Session, None, None]:
    """
    Shared requests session for API tests.
    
    Using a session is more efficient than creating new connections
    for each request.
    """
    session = requests.Session()
    yield session
    session.close()


# @pytest.fixture
def rick_api_base_url() -> str:
    """Base URL for the Rick and Morty API."""
    return "https://rickandmortyapi.com/api"


@pytest.fixture(autouse=True)
def enable_request_warnings():
    """Enable warnings for requests (useful for debugging)."""
    # Configure any global test settings here
    pass


# Pytest configuration
def pytest_configure(config):
    """Configure pytest with custom markers."""
    config.addinivalue_line(
        "markers", "api: mark test as an API integration test"
    )
    config.addinivalue_line(
        "markers", "slow: mark test as slow running"
    )


def pytest_collection_modifyitems(config, items):
    """Automatically add markers to tests based on naming patterns."""
    for item in items:
        # Add 'api' marker to tests that make HTTP requests
        if "api" in item.nodeid.lower():
            item.add_marker(pytest.mark.api)

