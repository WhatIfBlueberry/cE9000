import sys
sys.path.insert(0, '..')
import energyWithJulien
import unittest

class TestFindNeighbors(unittest.TestCase):
    def test_find_direct_neighbors(self):
        matrix = [[[{'x': x, 'y': y, 'z': z, 'spin': 1} for z in range(10)] for y in range(10)] for x in range(10)]
        center = {'x': 5, 'y': 5, 'z': 5, 'spin': 1}
        energyWithJulien.find_neighbors(center, matrix, 1)
        self.assertEqual(len(center['neighbors']), 6)

    def test_find_neighbors_range2(self):
        matrix = [[[{'x': x, 'y': y, 'z': z, 'spin': 1} for z in range(10)] for y in range(10)] for x in range(10)]
        center = {'x': 5, 'y': 5, 'z': 5, 'spin': 1}
        energyWithJulien.find_neighbors(center, matrix, 2)
        self.assertEqual(len(center['neighbors']), 32)

    def test_find_neighbors_range3(self):
        matrix = [[[{'x': x, 'y': y, 'z': z, 'spin': 1} for z in range(10)] for y in range(10)] for x in range(10)]
        center = {'x': 5, 'y': 5, 'z': 5, 'spin': 1}
        energyWithJulien.find_neighbors(center, matrix, 3)
        self.assertEqual(len(center['neighbors']), 122)

    def test_find_direct_neighbors_in_corner(self):
        matrix = [[[{'x': x, 'y': y, 'z': z, 'spin': 1} for z in range(10)] for y in range(10)] for x in range(10)]
        center = {'x': 0, 'y': 0, 'z': 0, 'spin': 1}
        energyWithJulien.find_neighbors(center, matrix, 1)
        self.assertEqual(len(center['neighbors']), 3)

    def test_find_direct_neighbors_in_corner_for_distance_two(self):
        matrix = [[[{'x': x, 'y': y, 'z': z, 'spin': 1} for z in range(3)] for y in range(3)] for x in range(3)]
        center = {'x': 0, 'y': 0, 'z': 0, 'spin': 1}
        energyWithJulien.find_neighbors(center, matrix, 2)
        self.assertEqual(len(center['neighbors']), 10)

    def test_find_direct_neighbors_in_corner_for_left_side_cutoff(self):
        matrix = [[[{'x': x, 'y': y, 'z': z, 'spin': 1} for z in range(10)] for y in range(10)] for x in range(10)]
        center = {'x': 5, 'y': 5, 'z': 0, 'spin': 1}
        energyWithJulien.find_neighbors(center, matrix, 3)
        self.assertEqual(len(center['neighbors']), 75)

if __name__ == '__main__':
    unittest.main()