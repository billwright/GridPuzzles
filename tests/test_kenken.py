import unittest
from Kenken import Kenken
from Calculation_Group import Calculation_Group

simple_kenken = [
    ('/', 3, ['A1', 'A2']),
    ('-', 1, ['B1', 'C1']),
    ('/', 3, ['B2', 'B3']),
    ('/', 2, ['C2', 'C3']),
    ('', 2, ['A3'])
]


class Test_Kenken(unittest.TestCase):

    def test_creation(self):
        kenken = Kenken(simple_kenken)
        self.assertIsNotNone(kenken)
        self.assertEqual(kenken.size, 3)
        kenken.display()


if __name__ == '__main__':
    unittest.main()
