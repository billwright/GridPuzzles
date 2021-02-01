import unittest
from Group import Group
from Cell import Cell


# noinspection PyPep8Naming
class TestGroup(unittest.TestCase):

    def test_creation(self):
        A1 = Cell('A1', '1234')
        B1 = Cell('B1', '1234')
        C1 = Cell('C1', '1234')
        D1 = Cell('D1', '1234')

        group = Group('Row 1', [A1, B1, C1, D1])
        print(group)
        self.assertIsNotNone(group)
        self.assertEqual(4, len(group))


if __name__ == '__main__':
    unittest.main()
