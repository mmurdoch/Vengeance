import unittest

import vengeance


class InitTest(unittest.TestCase):

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
            ],
        })

        room_a = vengeance._find_room('Room A', rooms)
        self.assertEqual(1, len(room_a.exits))
        room_b = vengeance._find_room('Room B', rooms)
        self.assertEqual(0, len(room_b.exits))

if __name__ == '__main__':
    unittest.main()
