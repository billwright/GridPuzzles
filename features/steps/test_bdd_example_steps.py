import pytest
from pytest_bdd import scenario, scenarios, given, when, then, parsers

# Scenarios
scenarios('../pytest-bdd-example.feature')


# Fixtures
# @pytest.fixture
# def world():
#     return {'type': 'Numbrix'}


# Given Steps

@given('I say hi')
def print_hi():
    print('hi')


# World is defined in the conftest.py file where it is global to all step-def files

@given('I print the world')
def print_hi(world):
    print('In print_hi and the world is:', world)


@given(parsers.parse('I say "{phrase}"'))
def print_phrase(phrase):
    print('In print_phrase and the print_phrase is:', phrase)


@given(parsers.parse('I put "{name}" into the world'))
def _(world, name):
    """I put "Bill" into the world."""
    world[name] = name


@then(parsers.parse('the world contains "{added_name}"'))
def _(world, added_name):
    assert added_name in world
