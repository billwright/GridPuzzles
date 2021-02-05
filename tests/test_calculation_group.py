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
        self.assertEqual(['1', '2', '3'], group_cell.candidates)

        operator = '+'
        required_result = 7
        group_definition = (operator, required_result, ['A1', 'A2', 'A3'])
        puzzle_size = 4
        group = Calculation_Group(group_definition, puzzle_size)
        self.assertIsNotNone(group)
        self.assertEqual(3, len(group.cells))

        group_cell = group.cells[0]
        self.assertEqual(['1', '2', '3', '4'], group_cell.candidates)

    def test_reduce_on_2_cell_plus(self):
        operator = '+'
        required_result = 7
        group_definition = (operator, required_result, ['A1', 'A2'])
        puzzle_size = 4
        group = Calculation_Group(group_definition, puzzle_size)

        # Before reduction
        group_cell = group.cells[0]
        self.assertEqual(['1', '2', '3', '4'], group_cell.candidates)

        # After reduction
        reduced_cells = group.reduce()
        print(reduced_cells)
        self.assertEqual(['3', '4'], group_cell.candidates)

    def test_reduce_on_3_cell_plus(self):
        operator = '+'
        required_result = 7
        group_definition = (operator, required_result, ['A1', 'A2', 'A3'])
        puzzle_size = 4
        group = Calculation_Group(group_definition, puzzle_size)

        # Before reduction
        group_cell = group.cells[0]
        self.assertEqual(['1', '2', '3', '4'], group_cell.candidates)

        # After reduction
        reduced_cells = group.reduce()
        print(reduced_cells)
        self.assertEqual(['1', '2', '3', '4'], group_cell.candidates)

    def test_reduce_on_3_cell_multiply(self):
        operator = '*'
        required_result = 6
        group_definition = (operator, required_result, ['A1', 'A2', 'A3'])
        puzzle_size = 4
        group = Calculation_Group(group_definition, puzzle_size)

        # Before reduction
        group_cell = group.cells[0]
        self.assertEqual(['1', '2', '3', '4'], group_cell.candidates)

        # After reduction
        reduced_cells = group.reduce()
        print(reduced_cells)
        self.assertEqual(['1', '2', '3'], group_cell.candidates)

        # Now let's try a 6x6 puzzle with the same group
        puzzle_size = 6
        group = Calculation_Group(group_definition, puzzle_size)

        # Before reduction
        group_cell = group.cells[0]
        self.assertEqual(['1', '2', '3', '4', '5', '6'], group_cell.candidates)

        # After reduction
        reduced_cells = group.reduce()
        print(reduced_cells)
        self.assertEqual(['1', '2', '3', '6'], group_cell.candidates)

    def test_reduce_on_subtraction(self):
        operator = '-'
        required_result = 3
        group_definition = (operator, required_result, ['A1', 'A2'])
        puzzle_size = 4
        group = Calculation_Group(group_definition, puzzle_size)

        # After reduction
        reduced_cells = group.reduce()
        print(reduced_cells)
        self.assertEqual(['1', '4'], reduced_cells[0].candidates)

        # Now let's try a 6x6 puzzle with the same group
        puzzle_size = 6
        required_result = 4
        group_definition = (operator, required_result, ['A1', 'A2'])
        group = Calculation_Group(group_definition, puzzle_size)

        # After reduction
        reduced_cells = group.reduce()
        print(reduced_cells)
        self.assertEqual(['1', '2', '5', '6'], reduced_cells[0].candidates)

    def test_reduce_on_division(self):
        operator = '/'
        required_result = 3
        group_definition = (operator, required_result, ['A1', 'A2'])
        puzzle_size = 4
        group = Calculation_Group(group_definition, puzzle_size)

        # After reduction
        reduced_cells = group.reduce()
        print(reduced_cells)
        self.assertEqual(['1', '3'], reduced_cells[0].candidates)

        # Now let's try a 6x6 puzzle with the same group
        puzzle_size = 6
        required_result = 3
        group_definition = (operator, required_result, ['A1', 'A2'])
        group = Calculation_Group(group_definition, puzzle_size)

        # After reduction
        reduced_cells = group.reduce()
        print(reduced_cells)
        self.assertEqual(['1', '2', '3', '6'], reduced_cells[0].candidates)


if __name__ == '__main__':
    unittest.main()
