import unittest
from Numbrix_Cell import Numbrix_Cell
from Chain_Endpoint import Chain_Endpoint


# noinspection PyPep8Naming
class TestChainEndpointCell(unittest.TestCase):

    def test_creation(self):

        endpoint_cell_E3 = Numbrix_Cell('E3', [63])
        cell_F3 = Numbrix_Cell('F3', [])
        cell_E4 = Numbrix_Cell('E4', [])
        cell_D3 = Numbrix_Cell('D3', [18])
        cell_E2 = Numbrix_Cell('E2', [64])
        neighbors_of_E3 = [cell_E4, cell_F3, cell_E2, cell_D3]

        endpoint_cell_G6 = Numbrix_Cell('G6', [54])
        endpoint_cell_H3 = Numbrix_Cell('H3', [74])
        endpoint_cell_H5 = Numbrix_Cell('H5', [78])

        all_endpoints = [endpoint_cell_H5, endpoint_cell_H3, endpoint_cell_G6, endpoint_cell_E3]

        # E3 has four neighbor cells, but two are solved and one is
        # chained to E3, so it has two open cells and needs 62 to be
        # in one of them. The Chain_Endpoint_Cell calculates all that.
        endpoint_cell = Chain_Endpoint(endpoint_cell_E3, neighbors_of_E3, all_endpoints)

        self.assertEqual(62, endpoint_cell.required_neighbor_values)

        self.assertTrue(cell_E4 in endpoint_cell.open_neighbors)
        self.assertTrue(cell_F3 in endpoint_cell.open_neighbors)
        self.assertFalse(cell_E2 in endpoint_cell.open_neighbors)
        self.assertFalse(cell_D3 in endpoint_cell.open_neighbors)

        self.assertEqual()


if __name__ == '__main__':
    unittest.main()
