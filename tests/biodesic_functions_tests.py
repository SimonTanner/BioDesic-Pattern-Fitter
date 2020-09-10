import unittest, sys, os

sys.path.append(os.getcwd())
from biodesic_functions import *

class TestRotateFunction(unittest.TestCase):

    def round_coords(self, coords):
        coords = list(map(lambda a: round(a, 2), coords))
        return coords

    def test_vector_no_offset(self):
        coords = [1, 1, 0]

        # Test rotating around x-axis
        ang = [90, 0, 0]
        rotated_coords = rotate_data(coords, ang)
        rotated_coords = self.round_coords(rotated_coords)
        self.assertEqual(rotated_coords, [1.0, 0.0, 1.0])

        # Test rotating around y-axis
        ang = [0, 90, 0]
        rotated_coords = rotate_data(coords, ang)
        rotated_coords = self.round_coords(rotated_coords)
        self.assertEqual(rotated_coords, [0.0, 1.0, 1.0])

        # Test rotating around z-axis
        ang = [0, 0, 90]
        rotated_coords = rotate_data(coords, ang)
        rotated_coords = self.round_coords(rotated_coords)
        self.assertEqual(rotated_coords, [-1.0, 1.0, 0])


    def test_vector_with_offset(self):
        coords = [0, 1, 1]
        offset = [1, 1, 0]
        
        # Test rotating around x-axis
        ang = [-90, 0, 0]
        rotated_coords = rotate_data(coords, ang, offset)
        rotated_coords = self.round_coords(rotated_coords)
        self.assertEqual(rotated_coords, [0.0, 2.0, 0.0])

        # Test rotating around y-axis
        ang = [0, 90, 0]
        rotated_coords = rotate_data(coords, ang, offset)
        rotated_coords = self.round_coords(rotated_coords)
        self.assertEqual(rotated_coords, [2.0, 1.0, -1.0])

        # Test rotating around z-axis
        ang = [0, 0, 90]
        rotated_coords = rotate_data(coords, ang, offset)
        rotated_coords = self.round_coords(rotated_coords)
        self.assertEqual(rotated_coords, [1.0, 0.0, 1.0])

if __name__ == '__main__':
    unittest.main()