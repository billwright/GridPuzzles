import math

import pytest
from puzzle_service import *
import json
import math

def generate_results_dictionary(puzzle_def):
    list_def = Numbrix.create_definition_from_string(puzzle_def)
    numbrix = Numbrix(list_def)
    results = {'given': numbrix.get_raw_dictionary()}
    solved_puzzle = numbrix.search().get_raw_dictionary()
    results['solution'] = solved_puzzle
    return results


definition = ",15,10,9,8,,17,,,,,6,18,,12,3,,1,19,,25,26,,30,20,,,,,31,,22,35,34,33,"
solution = generate_results_dictionary(definition)

definition_2 = ",,,,,,,28,25,22,19,,,27,26,21,20,,,34,35,12,13,,,3,36,11,10,,,,,,,"
solution_2 = generate_results_dictionary(definition_2)

PUZZLE_FILE_NAME = "../puzzles_test.json"


@pytest.fixture(autouse=True)
def run_before_and_after_tests(tmpdir):
    """Fixture to execute asserts before and after a test is run"""
    # Setup: fill with any logic you want
    with open(PUZZLE_FILE_NAME, 'w') as puzzle_file:
        json.dump({}, puzzle_file)

    yield  # this is where the testing happens

    # Teardown : fill with any logic you want


def test_reading_puzzle_file():
    assert_num_puzzles_in_puzzle_file(0)


def test_adding_existing_puzzle_to_file():
    store_puzzle_in_puzzle_file(definition, solution, PUZZLE_FILE_NAME)
    assert_num_puzzles_in_puzzle_file(1)

    # Here we try to add in the same puzzle
    store_puzzle_in_puzzle_file(definition, solution, PUZZLE_FILE_NAME)
    assert_num_puzzles_in_puzzle_file(1)

    # Now we'll add a new puzzle
    store_puzzle_in_puzzle_file(definition_2, solution_2, PUZZLE_FILE_NAME)
    assert_num_puzzles_in_puzzle_file(2)


def assert_num_puzzles_in_puzzle_file(num_puzzles):
    with open(PUZZLE_FILE_NAME, 'r') as puzzle_file:
        # Reading from json file
        # This file contains a dictionary of puzzles, keyed by the definition with a value of the solution
        puzzle_map = json.load(puzzle_file)
        print(puzzle_map)
        assert len(puzzle_map) == num_puzzles


def generate_results_dictionary(puzzle_def):
    list_def = Numbrix.create_definition_from_string(puzzle_def)
    numbrix = Numbrix(list_def)
    results = {'given': numbrix.get_raw_dictionary()}
    solved_puzzle = numbrix.search().get_raw_dictionary()
    results['solution'] = solved_puzzle
    return results


def test_puzzle_retrieval():
    puzzle_type = 'numbrix'
    dimension = 6
    # puzzle_map = retrieve_random_puzzle(puzzle_type, dimension)
    # assert puzzle_map is not None


def reorg_puzzle_file(puzzle_type, file_to_reorg):
    # I want a separate file for each puzzle type. It will contain a dictionary keyed by dimension
    # and then by puzzle definition string.
    with open(file_to_reorg, 'r') as puzzle_file:
        # Reading from json file
        # This file contains a dictionary of puzzles, keyed by the definition with a value of the solution
        puzzle_maps = json.load(puzzle_file)

    new_map = {}
    for key in puzzle_maps.keys():
        puzzle_map = puzzle_maps[key]
        curr_dim = int(math.sqrt(len(puzzle_map['solution'])))
        dim_map = {}
        if curr_dim in new_map.keys():
            dim_map = new_map[curr_dim]
        dim_map[key] = puzzle_map
        new_map[curr_dim] = dim_map

    with open(f'{puzzle_type}_puzzles.json', "w") as new_puzzle_file:
        json.dump(new_map, new_puzzle_file)

reorg_puzzle_file('numbrix', 'puzzles.json')