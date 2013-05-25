import unittest

import vengeance
from vengeance import game


class InitTest(unittest.TestCase):

    def test_matching_direction_name_and_opposite_throws(self):
        self.assert_game_throws({
            'directions': [
                {'name': 'up', 'opposite': 'up'}
            ],
            'rooms': []
        }, 'Redefined direction "up" as opposite of "up"')

    def test_non_unique_direction_name_throws(self):
        self.assert_game_throws({
            'directions': [
                {'name': 'east', 'opposite': 'west'},
                {'name': 'east', 'opposite': 'north'}
            ],
            'rooms': []
        }, 'Redefined direction name "east"')

    def test_direction_name_redefined_as_opposite_throws(self):
        self.assert_game_throws({
            'directions': [
                {'name': 'north', 'opposite': 'south'},
                {'name': 'west', 'opposite': 'north'}
            ],
            'rooms': []
        }, 'Redefinition of direction name "north" as an opposite')

    # test_missing_name_in_direction_throws
    # test_missing_opposite_in_direction_throws
    # test_use_of_quit_as_direction_throws
    # test_undefined_room_in_exit_throws
    # test_missing_name_in_room_throws
    # test_missing_description_in_room_throws

    def assert_game_throws(self, game_data, expected_message):
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
