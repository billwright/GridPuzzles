import unittest
from NumbrixCell import NumbrixCell
from Path import Path


# noinspection PyPep8Naming
class TestPath(unittest.TestCase):

    def test_creation(self):
        endpoints = [NumbrixCell('A1', [5]), NumbrixCell('B2', [7])]
        path = Path(endpoints[0], endpoints[1])
        assert path.value_distance == 2
        assert path.minimum_address_distance == 2

    def test_sorting_based_on_distance(self):
        path_distance_3_routes_1 = Path(NumbrixCell('A1', [1]), NumbrixCell('A4', [4]))
        path_distance_3_routes_1.routes = [(1, 2)]

        path_distance_4_routes_1 = Path(NumbrixCell('B1', [11]), NumbrixCell('B5', [15]))
        path_distance_4_routes_1.routes = [(11, 12)]

        path_distance_5_routes_1 = Path(NumbrixCell('C1', [21]), NumbrixCell('C6', [26]))
        path_distance_5_routes_1.routes = [(21, 22)]

        paths = [path_distance_5_routes_1, path_distance_3_routes_1, path_distance_4_routes_1]
        sorted_paths = Path.sort_by_least_routes(paths)

        print(sorted_paths)

        assert sorted_paths[0] == path_distance_5_routes_1
        assert sorted_paths[1] == path_distance_4_routes_1
        assert sorted_paths[2] == path_distance_3_routes_1

    def test_sorting_based_on_distance_and_routes(self):
        path_distance_3_routes_2 = Path(NumbrixCell('A1', [1]), NumbrixCell('A4', [4]))
        path_distance_3_routes_2.routes = [(1, 2), (3, 4)]

        path_distance_4_routes_1 = Path(NumbrixCell('B1', [11]), NumbrixCell('B5', [15]))
        path_distance_4_routes_1.routes = [(11, 12)]

        path_distance_5_routes_3 = Path(NumbrixCell('C1', [21]), NumbrixCell('C6', [26]))
        path_distance_5_routes_3.routes = [(21, 22), (31, 32), (41, 42)]

        paths = [path_distance_5_routes_3, path_distance_3_routes_2, path_distance_4_routes_1]
        sorted_paths = Path.sort_by_least_routes(paths)

        print(sorted_paths)

        assert sorted_paths[0] == path_distance_4_routes_1
        assert sorted_paths[1] == path_distance_3_routes_2
        assert sorted_paths[2] == path_distance_5_routes_3

    def test_sorting_based_on_distance_and_routes_some_none(self):
        path_distance_3_routes_none = Path(NumbrixCell('A1', [1]), NumbrixCell('A4', [4]))
        path_distance_3_routes_none.routes = None

        path_distance_5_routes_none = Path(NumbrixCell('D1', [1]), NumbrixCell('D6', [6]))
        path_distance_5_routes_none.routes = None

        path_distance_4_routes_1 = Path(NumbrixCell('B1', [11]), NumbrixCell('B5', [15]))
        path_distance_4_routes_1.routes = [(11, 12)]

        path_distance_6_routes_1 = Path(NumbrixCell('E1', [11]), NumbrixCell('E7', [17]))
        path_distance_6_routes_1.routes = [(11, 12)]

        path_distance_5_routes_3 = Path(NumbrixCell('C1', [21]), NumbrixCell('C6', [26]))
        path_distance_5_routes_3.routes = [(21, 22), (31, 32), (41, 42)]

        paths = [path_distance_6_routes_1, path_distance_5_routes_none,
                 path_distance_5_routes_3, path_distance_3_routes_none,
                 path_distance_4_routes_1]
        sorted_paths = Path.sort_by_least_routes(paths)

        print(sorted_paths)

        assert sorted_paths[0] == path_distance_6_routes_1
        assert sorted_paths[1] == path_distance_4_routes_1
        assert sorted_paths[2] == path_distance_5_routes_3
        assert sorted_paths[3] == path_distance_3_routes_none
        assert sorted_paths[4] == path_distance_5_routes_none
