import unittest, sys, os

sys.path.append(os.getcwd())
from biodesic_fit_version_1 import *

class TestModelCoordsConvertor(unittest.TestCase):

    def test_simple(self):
        coords = [100, 100, 100]
        scale = 0.5
        centre_point = [100, 100, 100]
        screen_dims = (200, 200)
        angle = (0, 0, 0)
        
        scr_coords = model_coords_convertor(coords, scale, centre_point, screen_dims, angle)
        exp_coords = [100, 100]
        self.assertEqual(scr_coords, exp_coords)

        coords = [100, 100, 100]
        scale = 0.5
        centre_point = [0, 0, 0]
        screen_dims = (200, 200)
        
        scr_coords = model_coords_convertor(coords, scale, centre_point, screen_dims, angle)
        exp_coords = [50, 50]
        self.assertEqual(scr_coords, exp_coords)



if __name__ == '__main__':
    unittest.main()