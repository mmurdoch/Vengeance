import unittest

from vengeance.game import Direction
from vengeance.game import Game
from vengeance.game import Location
from vengeance.game import PlayerCharacter


class DirectionTest(unittest.TestCase):
    def test_setting_opposite(self):
        east = Direction('east')
        west = Direction('west')

        east.opposite = west

        self.assertEquals(west.name, east.opposite.name)

    def test_setting_opposite_also_sets_reverse(self):
        east = Direction('east')
        west = Direction('west')

        east.opposite = west

        self.assertEquals(east.name, west.opposite.name)


class GameTest(unittest.TestCase):
    def test_find_location(self):
        name = 'Arbitrary name'
        description = 'Arbitrary description'
        game = Game([Location(name, description)])

        location = game.find_location(name)

        self.assertEqual(description, location.description)

    def test_first_location_is_character_start(self):
        first_location_name = 'one'
        first_location = Location(first_location_name)
        second_location = Location('two')
        game = Game([first_location, second_location])

        starting_location = game.character.current_location

        self.assertEqual(first_location_name, starting_location.name)

    def test_movement(self):
        location_one = Location('L1')
        location_two = Location('L2')
        location_one.add_one_way_exit(Direction('west'), location_two)
        game = Game([location_one, location_two])

        game.process_input('w')

        self.assertEqual('L2', game.character.current_location.name)

    def test_process_input_command_by_name(self):
        quit_called = {'yes': False}
        game = self._arbitrary_game(quit_called)
        quit_command_name = 'quit'

        game.process_input(quit_command_name)

        self.assertTrue(quit_called['yes'])

    def test_process_input_command_by_synonym(self):
        quit_called = {'yes': False}
        game = self._arbitrary_game(quit_called)

        game.process_input('q')

        self.assertTrue(quit_called['yes'])

    def test_unrecognised_input_ignored(self):
        game = self._arbitrary_game()

        game.process_input('unrecognised')

    def test_process_input_matching_multiple_commands_ignored(self):
        location_one = Location('L1')
        location_two = Location('L2')
        location_one.add_one_way_exit(Direction('quick'), location_two)
        game = Game([location_one, location_two])

        game.process_input('q')

    def test_no_locations_throws(self):
        try:
            Game([])
            self.fail()
        except ValueError:
            # Success
            pass

    def test_run_renders_current_location(self):
        game = self._arbitrary_game()

        rendered_location = {}

        def location_renderer(location):
            rendered_location['location'] = location

        game.location_renderer = location_renderer

        def display_handler(text):
            pass

        game.display_handler = display_handler

        def quit_input_provider():
            return 'q'

        game.input_handler = quit_input_provider

        def quit_immediately(display_handler, input_handler):
            return True

        game.quit_handler = quit_immediately
        game.run()

        self.assertEqual(game.character.current_location.name,
                         rendered_location['location'].name)

    def test_render_with_no_exits(self):
        location = Location(self.arbitrary_name)
        game = Game([location])

        self.assertEqual(self.arbitrary_name + " (exits: <none>)",
                         self.render(game, location))

    def test_render_with_one_exit(self):
        location = Location(self.arbitrary_name)

        location.add_one_way_exit(Direction('north'), location)

        game = Game([location])

        self.assertEqual(self.arbitrary_name + " (exits: north)",
                         self.render(game, location))

    def test_render_with_two_exits(self):
        location = Location(self.arbitrary_name)

        location.add_one_way_exit(Direction('north'), location)
        location.add_one_way_exit(Direction('south'), location)

        game = Game([location])

        self.assertEqual(self.arbitrary_name + " (exits: north, south)",
                         self.render(game, location))

    def test_render_with_description(self):
        location = Location(self.arbitrary_name, self.arbitrary_description)
        game = Game([location])

        self.assertEqual(self.arbitrary_name + " (exits: <none>)\n" +
                         self.arbitrary_description,
                         self.render(game, location))

    def render(self, game, location):
        return game.location_renderer(location)

    @property
    def arbitrary_name(self):
        return 'arbitrary name'

    @property
    def arbitrary_description(self):
        return 'arbitrary description'

    def _arbitrary_game(self, quit_called={}):
        game = Game([Location('L1', '')])

        def quit_handler(display_handler, input_handler):
            quit_called['yes'] = True
            return True

        game.quit_handler = quit_handler
        return game


class LocationTest(unittest.TestCase):
    def test_name(self):
        name = 'a name'
        location = Location(name, self.arbitrary_description)

        self.assertEqual(name, location.name)

    def test_description(self):
        description = self.arbitrary_description
        location = Location(self.arbitrary_name, description)

        self.assertEqual(description, location.description)

    def test_default_description_is_empty_string(self):
        location = Location(self.arbitrary_name)

        self.assertEqual('', location.description)

    def test_add_exit_with_no_opposite_throws(self):
        direction = Direction('up')
        location1 = Location(self.arbitrary_name)
        location2 = Location(self.arbitrary_name + '2')

        try:
            location1.add_exit(direction, location2)
            self.fail()
        except ValueError:
            # Success
            pass

    @property
    def arbitrary_name(self):
        return 'arbitrary name'

    @property
    def arbitrary_description(self):
        return 'arbitrary description'


if __name__ == '__main__':
    unittest.main()
