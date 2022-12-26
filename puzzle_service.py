from flask import Flask, request
from Numbrix import Numbrix
from flask import send_from_directory
from Inconsistent_Puzzle_Exception import Inconsistent_Puzzle_Exception

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
        return results
    except Exception:
        return 'Inconsistent Puzzle', 400


@app.route('/solve/sudoku', methods=['GET'])
def solve_sudoku():
    return 'Solving sudoku...not yet implemented'


@app.route('/solve/kenken', methods=['GET'])
def solve_kenken():
    return 'Solving kenken...not yet implemented'

    # response = app.response_class(
    #         response=json.dumps(data),
    #         status=200,
    #         mimetype='application/json'
    #     )
    #     return response
