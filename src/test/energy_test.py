import sys
sys.path.insert(0, '..')

import unittest
import numpy as np
import energy


class TestEnergy(unittest.TestCase):
    def setUp(self):
        self.spins = np.array([[[-1, 1, -1], [1, -1, 1], [-1, 1, -1]],
                       [[1, -1, 1], [-1, 1, -1], [1, -1, 1]],
                       [[-1, 1, -1], [1, -1, 1], [-1, 1, -1]]])
        self.interactionDistance = 1

    def test_ce9000(self):
        result = energy.ce9000(self.spins, self.interactionDistance)
        self.assertEqual(result, 54)

    def test_energyOfSpinAtPos(self):
        result = energy.energyOfSpinAtPos(1, 1, 1, self.spins, self.interactionDistance)
        self.assertEqual(result, 6)

    def test_deltaE(self):
        result = energy.deltaE(1, 1, 1, self.spins, self.interactionDistance)
        self.assertEqual(result, -12)

if __name__ == '__main__':
    unittest.main()