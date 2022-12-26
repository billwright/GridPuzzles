import pytest
from pytest_bdd import scenario, scenarios, given, when, then

# Scenarios
scenarios('../features/numbrix.feature')


# Fixtures
@pytest.fixture
def world():
    return {'type': 'Numbrix'}


# Given Steps

@given('I say hi')
def print_hi(world):
    print('hi')
    print(world['type'])
