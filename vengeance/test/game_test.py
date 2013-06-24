import unittest

from vengeance.game import Location


class GameTest(unittest.TestCase):
    def test_find_location(self):
        pass


class LocationTest(unittest.TestCase):
    def test_description(self):
        description = "a description"
        location = Location("arbitrary name", description)

        self.assertEqual(description, location.description)

if __name__ == '__main__':
    unittest.main()
