import unittest
from grid_utils import cross
from grid_utils import super_cross


class TestGridUtils(unittest.TestCase):

    def test_cross(self):
        crossed = cross('123', '123')
        self.assertEqual(9, len(crossed))

        crossed = cross('12', '123')
        self.assertEqual(6, len(crossed))

    def test_super_cross(self):
        candidates = [['1', '2', '3'], ['1', '2', '3'], ['1', '2', '3']]
        super_crossed = super_cross(candidates)
        self.assertEqual(27, len(super_crossed))

        candidates = [['1', '2', '3'], ['1', '2', '3'], ['1', '2', '3'], ['4', '5']]
        super_crossed = super_cross(candidates)
        self.assertEqual(54, len(super_crossed))


if __name__ == '__main__':
    unittest.main()
