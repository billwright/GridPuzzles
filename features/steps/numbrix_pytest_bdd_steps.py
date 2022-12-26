import pytest
from pytest_bdd import scenario, scenarios, given, when, then, parsers

# Scenarios
scenarios('../numbrix.feature')


@given("the puzzle server is running")
def server_is_running(world):
    pass


@given("the following Numbrix puzzle")
def the_given_numbrix(world):


@when('I submit this puzzle to the solver')
def solve_numbrix(context):
    print(f'\nGiven string is {context.given}: {len(context.given)} characters\n\n')


@then('I get the following result back')
def check_results(context):
    print('in check_results')
    assert len(context.given) == 431
