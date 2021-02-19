#!/bin/bash

echo "Running all tests"

export PYTHONPATH=.:tests/

#python tests/test_calculation_group.py
#python tests/test_cell.py
#python tests/test_grid_utils.py
#python tests/test_group.py
#python tests/test_puzzle_creation.py
#python tests/test_matchlet.py
python tests/test_kenken.py
python tests/test_numbrix.py
python tests/test_sudoku.py
