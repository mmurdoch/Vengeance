import unittest

from vengeance.game import Direction
from vengeance.game import Game
from vengeance.game import Location


class GameTest(unittest.TestCase):
    def test_find_location(self):
        name = 'Arbitrary name'
        description = 'Arbitrary description'
        locations = [Location(name, description)]
        game = Game(locations)

        location = game.find_location(name)

        self.assertEqual(description, location.description)

    def test_first_location_is_character_start(self):
        first_location_name = 'one'
        first_location = Location(first_location_name, 'one')
        second_location = Location('two', 'two')
        game = Game([first_location, second_location])

        starting_location = game.character.current_location

        self.assertEqual(first_location_name, starting_location.name)

    def test_movement(self):
        location_one = Location('L1', '')
        location_two = Location('L2', '')
        location_one.add_one_way_exit(Direction('west'), location_two)
        game = Game([location_one, location_two])

        game.process_input('w')

        self.assertEqual('L2', game.character.current_location.name)

    # def test_find_command_by_name
    # def test_find_command_by_synonym
    # def_test_find_clashing_command
    # def_test_missing_command
    # def_test_find_command_includes_location_commands


class LocationTest(unittest.TestCase):
    def test_name(self):
        name = 'a name'
        location = Location(name, 'arbitrary description')

        self.assertEqual(name, location.name)

    def test_description(self):
        description = 'a description'
        location = Location('arbitrary name', description)

        self.assertEqual(description, location.description)

if __name__ == '__main__':
    unittest.main()
