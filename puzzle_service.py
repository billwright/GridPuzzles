from flask import Flask, request
from Numbrix import Numbrix
from flask import send_from_directory
import json
from Already_Solved_Exception import Already_Solved_Exception

# Start the flask service with this command (in the same directory as this file):  flask --app puzzle_service run

PUZZLE_FILE_NAME = "puzzles.json"

app = Flask(__name__,
            static_url_path='',
            static_folder='web',
            template_folder='web/templates')


@app.route('/')
def home():
    return send_from_directory('web', 'index.html')


@app.route('/welcome')
def welcome():
    return "My Puzzle-Solving Server"


@app.route('/solve/numbrix', methods=['GET'])
def solve_numbrix():
    if 'definition' not in request.args:
        return 'To solve numbrix, pass me a puzzle definition.'

    puzzle_def = request.args['definition']
    if puzzle_def[-1] == ',':
        puzzle_def = puzzle_def[0:-1]
        print('Adjusting the puzzle definition by trimming a trailing comma...')

    print('In solve_numbrix and trying to solve this puzzle definition:', puzzle_def)

    try:
        list_def = Numbrix.create_definition_from_string(puzzle_def)
        numbrix = Numbrix(list_def)
        results = {'given': numbrix.get_raw_dictionary()}
        solved_puzzle = numbrix.search().get_raw_dictionary()
        results['solution'] = solved_puzzle

        print('Storing this puzzle definition and the solution for future use', puzzle_def, solved_puzzle)
        store_puzzle_in_puzzle_file(puzzle_def, results, PUZZLE_FILE_NAME)

        return results

    except Already_Solved_Exception as e:
        return 'Already solved', 200
    except Exception as e:
        print('Error! The error was:', e)
        return 'Inconsistent Puzzle', 500


@app.route('/solve/sudoku', methods=['GET'])
def solve_sudoku():
    return 'Solving sudoku...not yet implemented', 400


@app.route('/solve/kenken', methods=['GET'])
def solve_kenken():
    return 'Solving kenken...not yet implemented', 400

    # response = app.response_class(
    #         response=json.dumps(data),
    #         status=200,
    #         mimetype='application/json'
    #     )
    #     return response


# Wouldn't it be great if all puzzles entered via the UI were saved, so that we could offer up puzzles for users
# to solve? Yes, it would. So, let's save them all to a JSON file, along with a solution, though I'm not sure why
# I'd save the solution, as the server can just solve it... Maybe to give random hints? Okay. So, the file format
# will be like this:
#
# {
#    ",15,10,9,8,,17,,,,,6,18,,12,3,,1,19,,25,26,,30,20,,,,,31,,22,35,34,33,,":
#     "16,15,10,9,8,7,17,14,11,4,5,6,18,13,12,3,2,1,19,24,25,26,29,30,20,23,36,27,28,31,21,22,35,34,33,32,",
#    "another puzzle definition":
# ]
#
# We'll name the file puzzles.json and just store it in this directory for now

def store_puzzle_in_puzzle_file(definition, solution, puzzle_file_name):
    with open(puzzle_file_name, 'r') as puzzle_file:
        # This file contains a dictionary of puzzles, keyed by the definition with a value of the solution
        puzzle_map = json.load(puzzle_file)

    if definition not in puzzle_map.keys():
        puzzle_map[definition] = solution
        with open(puzzle_file_name, "w") as new_puzzle_file:
            json.dump(puzzle_map, new_puzzle_file)
    else:
        print('I am not saving this puzzle, as I have seen it before.')

