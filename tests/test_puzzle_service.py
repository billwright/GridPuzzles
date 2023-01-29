# These tests are for our puzzle service. We start with some rudimentary tests
def test_request_with_no_puzzle_type(client):
    response = client.get("/new_puzzle")
    assert b'To get a new puzzle, you must pass the puzzle type.' in response.data


def test_request_with_no_dimension(client):
    response = client.get("/new_puzzle", query_string={"puzzle_type": "numbrix"})
    assert b'To get a new puzzle, you must pass the dimension.' in response.data


def test_request_new_puzzle(client):
    response = client.get("/new_puzzle", query_string={"puzzle_type": "numbrix", "dimension": 6})
    assert b'given' in response.data
