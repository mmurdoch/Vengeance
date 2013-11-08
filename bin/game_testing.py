# Use case: Testing a game built with the engine
# Example:
import unittest

import vengeance

class MyAdventureGameTest(unittest.TestCase):
    def test_navigation(self):
        # Use declaratively defined game but could just as easily be
        # created procedurally
        game = vengeance.create_game({
            'directions': [
                {'name': 'up', 'opposite': 'down'},
                {'name': 'in', 'opposite': 'out'},
                {'name': 'west', 'opposite': 'east'}
            ],
            'rooms': [
                {'name': 'A Church',
                 'description': 'Tiny place of worship',
                 'exits': [
                     {'to': 'The Crypt', 'direction': 'down'}
                 ]},
                {'name': 'The Crypt',
                 'description': 'Dusty tomb filled with empty sarcophagi',
                 'exits': [
                     {'to': 'A Coffin', 'direction': 'in', 'one_way': True},
                     {'to': 'A Cave', 'direction': 'west'}
                 ]},
                {'name': 'A Coffin',
                 'description': 'A tight squeeze and pitch dark'},
                {'name': 'A Cave',
                 'description': 'A dark and dingy place'}
            ],
        })

        commands = ['d', 'w', 'e', 'i']

        for command in commands:
            game.process_input(command)

        self.assertEquals('A Coffin', game.character.current_location.name)


if __name__ == '__main__':
    unittest.main()
