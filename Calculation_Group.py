from Group import Group
from Cell import Cell
from grid_utils import super_cross


class Calculation_Group(Group):

    def __init__(self, group_definition_tuple, puzzle_size):
        (operator, required_result, cell_addresses) = group_definition_tuple

        # Validate group
        self.validate_group_definition(operator, required_result, len(cell_addresses))

        # Set class instance variables
        self.operator = operator
        self.required_result = required_result

        # Create the cells for this group
        all_candidates = ''.join([str(i+1) for i in range(0, puzzle_size)])
        cells = [Cell(address, all_candidates) for address in cell_addresses]

        # Now call superclass initialization, which will set superclass instance variables
        name = 'Calculation - ' + ''.join(cell_addresses)
        super().__init__(name, cells)

    @staticmethod
    def validate_group_definition(operator, required_result, number_of_cells):
        if operator == '':
            if number_of_cells != 1:
                raise ValueError('It is invalid to have a group of 2 cells for the null operator')
            return str(required_result)

        if operator not in "+-/x":
            raise ValueError('The only valid operators are: + - / * ')

        if number_of_cells < 2:
            raise ValueError('It is invalid to have any group with one cell unless the operator is null')

        if operator in "-/" and number_of_cells != 2:
            raise ValueError('Subtraction and divide operators can only have two cells in the group')

    def reduce(self):
        # This method reduces the values in the group based on the mathematical operator
        #
        # The operator is one of: plus, minus, division, multiplication
        # The choices is a list of lists. One choice from each sublist must
        # be used to form the result. For example, if we call this function
        # with these values:
        #
        #   calculate_operands('+', ['1234', '1234'], 7)
        #
        # Then we return a list of the choices in each position which satisfy
        # this constrain. In this case the answer would be:
        #
        #   ['34', '34']
        #
        # Another example is:
        #
        #   calculate_operands('+', ['1234', '1234', '1234'], 9)
        #
        # return value:
        #
        #   ['1234', '1234', '1234']
        #
        # Another example is:
        #
        #   calculate_operands('*', ['123456', '123456', '123456'], 60)
        #
        # return value:
        #
        #   ['2345', '2345', '2345']
        #
        # Another example is:
        #
        #   calculate_operands('+', ['123456', '123456'], 3)
        #
        # return value:
        #
        #   ['12', '12']

        valid_operand_combinations = []
        all_operand_combinations = super_cross(self.get_all_candidates())
        for operand_combo in all_operand_combinations:
            eval_string = self.operator.join(operand_combo)
            result = eval(eval_string)
            if result == self.required_result:
                valid_operand_combinations.append(operand_combo)
        return valid_operand_combinations

