import unittest

import vengeance
from vengeance import game


class InitTest(unittest.TestCase):

    def test_game_data_none_throws(self):
        self.assert_run_game_throws(None, 'game_data must be a dictionary')

    def test_game_data_not_dictionary_throws(self):
        self.assert_run_game_throws([], 'game_data must be a dictionary')

    def test_missing_directions_throws(self):
        self.assert_run_game_throws({
        }, 'Missing directions list')

    def test_matching_direction_name_and_opposite_throws(self):
        self.assert_run_game_throws({
            'directions': [
                {'name': 'up', 'opposite': 'up'}
            ]
        }, 'Direction "up" cannot be its own opposite')

    def test_non_unique_direction_name_throws(self):
        self.assert_run_game_throws({
            'directions': [
                {'name': 'east', 'opposite': 'west'},
                {'name': 'east', 'opposite': 'north'}
            ]
        }, 'Redefinition of direction "east"')

    def test_non_unique_opposite_direction_throws(self):
        self.assert_run_game_throws({
            'directions': [
                {'name': 'up', 'opposite': 'down'},
                {'name': 'in', 'opposite': 'down'}
            ]
        }, 'Redefinition of direction "down" as an opposite')

    def test_direction_name_redefined_as_opposite_throws(self):
        self.assert_run_game_throws({
            'directions': [
                {'name': 'north', 'opposite': 'south'},
                {'name': 'west', 'opposite': 'north'}
            ]
        }, 'Redefinition of direction "north" as an opposite')

    def test_direction_opposite_redefined_as_name_throws(self):
        self.assert_run_game_throws({
            'directions': [
                {'name': 'in', 'opposite': 'out'},
                {'name': 'out', 'opposite': 'down'}
            ]
        }, 'Redefinition of direction "out"')

    def test_missing_direction_name_throws(self):
        self.assert_run_game_throws({
            'directions': [
                {'opposite': 'in'}
            ]
        }, 'Missing name from direction with opposite "in"')

    def test_missing_direction_opposite_throws(self):
        self.assert_run_game_throws({
            'directions': [
                {'name': 'west'}
            ]
        }, 'Missing opposite from direction with name "west"')

    def test_missing_name_and_opposite_from_direction_throws(self):
        self.assert_run_game_throws({
            'directions': [
                {}
            ]
        }, 'Missing name and opposite from direction')

    def test_direction_name_not_string_throws(self):
        self.assert_run_game_throws({
            'directions': [
                {'name': False, 'opposite': 'down'}
            ]
        }, 'Direction name must be a string')

    def test_direction_opposite_not_string_throws(self):
        self.assert_run_game_throws({
            'directions': [
                {'name': 'up', 'opposite': []}
            ]
        }, 'Direction opposite must be a string')

    def test_use_of_quit_as_direction_name_throws(self):
        self.assert_run_game_throws({
            'directions': [
                {'name': 'quit', 'opposite': 'north'}
            ]
        }, 'Direction name cannot use reserved word "quit"')

    def test_use_of_quit_as_direction_opposite_throws(self):
        self.assert_run_game_throws({
            'directions': [
                {'name': 'up', 'opposite': 'quit'}
            ]
        }, 'Direction opposite cannot use reserved word "quit"')

    def test_non_unique_room_name_throws(self):
        self.assert_run_game_throws({
            'directions': [],
            'rooms': [
                {'name': 'Entrance Hall', 'description': 'A description'},
                {'name': 'Entrance Hall', 'description': 'B description'}
            ]
        }, 'Redefinition of room "Entrance Hall"')

    def test_missing_rooms_throws(self):
        self.assert_run_game_throws({
            'directions': []
        }, 'Missing rooms list')

    def test_zero_rooms_throws(self):
        self.assert_run_game_throws({
            'directions': [],
            'rooms': []
        }, 'Rooms list must contain at least one room')

    def test_missing_room_name_throws(self):
        self.assert_run_game_throws({
            'directions': [],
            'rooms': [
                {'description': 'No name'}
            ]
        }, 'Missing name from room with description "No name"')

    def test_room_name_not_string_throws(self):
        self.assert_run_game_throws({
            'directions': [],
            'rooms': [
                {'name': {}, 'description': 'Bad name'}
            ]
        }, 'Room name must be a string')

    # test_missing_room_description_throws
    # test_room_description_not_string_throws
    # test_undefined_room_in_exit_throws

    def assert_run_game_throws(self, game_data, expected_message):
        try:
            vengeance.run_game(game_data)
            self.fail()
        except game.GameFormatException as e:
            self.assertEqual(expected_message, e.message)

    # Ah, this doesn't test the public API (and therefore won't work with
    # from vengeance import * - which Pylint complains about...)
    def test_one_way_exit(self):
        rooms = vengeance._load_rooms({
            'directions': [
                {'name': 'up', 'opposite': 'down'},
            ],
            'rooms': [
                {'name': 'Room A',
                 'description': 'A',
                 'exits': [
                     {'to': 'Room B', 'direction': 'down', 'one_way': True}
                 ]},
                {'name': 'Room B',
                 'description': 'B'
                 }
            ]
        })

        room_a = vengeance._find_room('Room A', rooms)
        self.assertEqual(1, len(room_a.exits))
        room_b = vengeance._find_room('Room B', rooms)
        self.assertEqual(0, len(room_b.exits))

if __name__ == '__main__':
    unittest.main()
