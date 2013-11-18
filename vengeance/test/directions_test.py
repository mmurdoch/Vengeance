import unittest

from vengeance.directions import *


class DirectionsTest(unittest.TestCase):
    def test_north_name(self):
        self.assertEqual('north', NORTH.name)

    def test_north_has_south_as_opposite(self):
        self.assertEqual(SOUTH, NORTH.opposite)

    def test_south_name(self):
        self.assertEqual('south', SOUTH.name)

    def test_south_has_north_as_opposite(self):
        self.assertEqual(NORTH, SOUTH.opposite)

    def test_east_name(self):
        self.assertEqual('east', EAST.name)

    def test_east_has_west_as_opposite(self):
        self.assertEqual(WEST, EAST.opposite)

    def test_west_name(self):
        self.assertEqual('west', WEST.name)

    def test_west_has_east_as_opposite(self):
        self.assertEqual(EAST, WEST.opposite)

    def test_in_name(self):
        self.assertEqual('in', IN.name)

    def test_in_has_out_as_opposite(self):
        self.assertEqual(OUT, IN.opposite)

    def test_out_name(self):
        self.assertEqual('out', OUT.name)

    def test_out_has_in_as_opposite(self):
        self.assertEqual(IN, OUT.opposite)

    def test_up_name(self):
        self.assertEqual('up', UP.name)

    def test_up_has_down_as_opposite(self):
        self.assertEqual(DOWN, UP.opposite)

    def test_down_name(self):
        self.assertEqual('down', DOWN.name)

    def test_down_has_up_as_opposite(self):
        self.assertEqual(UP, DOWN.opposite)


if __name__ == '__main__':
    unittest.main()
