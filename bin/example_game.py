import vengence

vengence.run_game({
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