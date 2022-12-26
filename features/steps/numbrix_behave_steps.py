from behave import *


@given("the following Numbrix puzzle")
def the_given_numbrix(context):
    print('The puzzle string is:', context.text)
    context.given = context.text


@when('I submit this puzzle to the solver')
def solve_numbrix(context):
    # print(f'Given string is {len(context.given)} characters long')
    print(f'\nGiven string is {context.given}: {len(context.given)} characters\n\n')


@then('I get the following result back')
def check_results(context):
    print('in check_results')
    assert len(context.given) == 431
