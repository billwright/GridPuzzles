import pytest
from pytest_bdd import scenario, scenarios, given, when, then


# Fixtures
@pytest.fixture
def world():
    return {'type': 'Numbrix'}
