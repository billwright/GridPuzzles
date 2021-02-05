import unittest
from Calculation_Group import Calculation_Group


class TestCalculationGroup(unittest.TestCase):

    def test_validate_group_definition(self):
        # First let's test the easiest one, the null operator
        operator = ''
        required_result = '2'
        number_of_cells = 1
        puzzle_size = 3
        candidates = Calculation_Group.validate_group_definition(operator, required_result, number_of_cells)
        self.assertEqual('2', candidates)

        number_of_cells = 2
        # It is invalid to have a group of 2 cells for the null operator
        with self.assertRaises(ValueError):
            Calculation_Group.validate_group_definition(operator, required_result, number_of_cells)

        number_of_cells = 1
        operator = '+'
        # It is invalid to have any group with one cell unless the operator is null
        with self.assertRaises(ValueError):
            Calculation_Group.validate_group_definition(operator, required_result, number_of_cells)

        operator = '?'
        # The only valid operators are: + - / *
        with self.assertRaises(ValueError):
            Calculation_Group.validate_group_definition(operator, required_result, number_of_cells)

    def test_group_creation(self):
        operator = '+'
        required_result = 3
        group_definition = (operator, required_result, ['A1', 'A2'])
        puzzle_size = 3
        group = Calculation_Group(group_definition, puzzle_size)
        self.assertIsNotNone(group)
        self.assertEqual(2, len(group.cells))

        group_cell = group.cells[0]
        self.assertEqual('123', group_cell.candidates)

        operator = '+'
        required_result = 7
        group_definition = (operator, required_result, ['A1', 'A2', 'A3'])
        puzzle_size = 4
        group = Calculation_Group(group_definition, puzzle_size)
        self.assertIsNotNone(group)
        self.assertEqual(3, len(group.cells))

        group_cell = group.cells[0]
        self.assertEqual('1234', group_cell.candidates)

    @unittest.skip
    def test_reduce(self):
        operator = '+'
        required_result = 7
        group_definition = (operator, required_result, ['A1', 'A2'])
        puzzle_size = 4
        group = Calculation_Group(group_definition, puzzle_size)

        # Before reduction
        group_cell = group.cells[0]
        self.assertEqual('1234', group_cell.candidates)

        # After reduction
        valid_combinations = group.reduce()
        self.assertEqual('34', group_cell.candidates)


if __name__ == '__main__':
    unittest.main()
