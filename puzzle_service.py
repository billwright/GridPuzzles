from flask import Flask, request
from Numbrix import Numbrix

app = Flask(__name__)


@app.route('/')
def welcome():
    return "Bill Wright's Puzzle-Solving Server"


@app.route('/solve/numbrix', methods=['GET'])
def solve_numbrix():
    puzzle_def = request.args['definition']

    list_def = Numbrix.create_definition_from_string(puzzle_def)
    numbrix = Numbrix(list_def)
    return numbrix.search().get_raw_dictionary()


@app.route('/solve/sudoku', methods=['GET'])
def solve_sudoku():
    return 'not yet implemented'


@app.route('/solve/kenken', methods=['GET'])
def solve_kenken():
    return 'not yet implemented'

    # response = app.response_class(
    #         response=json.dumps(data),
    #         status=200,
    #         mimetype='application/json'
    #     )
    #     return response
