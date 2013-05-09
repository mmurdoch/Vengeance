from __future__ import print_function
import sys

class Room:
    def __init__(self, name, description):
        self._commands = []
        self._exits = []
        self._name = name
        self._description = description
        
    def add_exit(self, direction, room):
        self.add_one_way_exit(direction, room)
        room.add_one_way_exit(direction.opposite, self)
    
    def add_one_way_exit(self, direction, room):
        self._exits.append(Exit(direction.name, room))
        exit_command = Command(direction.name, Player.move_to, room)
        exit_command.add_synonym(direction.name[0])
        self._commands.append(exit_command)

    @property
    def commands(self):
        return self._commands

    @property
    def exits(self):
        return self._exits
    
    @property
    def name(self):
        return self._name
    
    @property
    def description(self):
        return self._description

class Exit:
    def __init__(self, direction, to_room):
        self.direction = direction
        self.to_room = to_room

class Command:
    def __init__(self, name, func, context):
        self._name = name
        self._synonyms = []
        self._func = func
        self._context = context
    
    @property
    def name(self):
        return self._name

    def add_synonym(self, synonym):
    	self._synonyms.append(synonym)

    def matches(self, value):
        for synonym in self._synonyms:
            if synonym == value:
                return True

        return self.name == value

    def run(self, player):
        self._func(player, self._context)

class Player:
    def __init__(self, current_room):
        self.move_to(current_room)

    @property
    def current_room(self):
        return self._current_room
    
    def move_to(self, room):
        self._current_room = room

def quit_game(player, context):
    print("Are you sure you want to quit?")
    quit_input = raw_input()
    if quit_input == "y" or quit_input == "yes":
        sys.exit()

class Game:
    def __init__(self, starting_room):
        self.player = Player(starting_room)
        self._commands = []
        self.add_command(Command("quit", quit_game, None))

    def add_command(self, command):
        self._commands.append(command)

    def run(self):
        while (True):
            self._display_room(self.player.current_room)
            self._process_command(self._get_input())

    def _display_room(self, room):
        title = room.name
        title += " (exits: "
        if len(room.exits) == 0:
            title += "<none> "
        for exit in room.exits:
            title += exit.direction
            title += " "
        title += "\b"
        title += ")"
        print(title)
        print(room.description)

    def _get_input(self):
        return raw_input()
        
    def _process_command(self, user_input):
        for command in self._commands:
            if command.matches(user_input):
                command.run(self.player)
        
        room = self.player.current_room
        for command in room.commands:
            if command.matches(user_input):
                command.run(self.player)

class Direction:
    def __init__(self, name):
        self._name = name

    @property
    def name(self):
        return self._name

    @property
    def opposite(self):
        return self._opposite
        
    @opposite.setter
    def opposite(self, value):
        self._opposite = value

game_data = {
    'directions': [
        { 'name': 'up', 'opposite': 'down' }
    ],
    'rooms': [
        { 'name': 'A Church', 'description': 'Tiny place of worship'},
        { 'name': 'The Crypt', 'description': 'Dusty tomb filled with empty sarcophagi'}
    ],
    # Why can't this be with room data?
    'exits': [
        { 'from': 'A Church', 'to': 'The Crypt', 'direction': 'down'}
    ]
}

direction_data = game_data['directions']

room_data = game_data['rooms']

exit_data = game_data['exits']

directions = []
for datum in direction_data:
    direction = Direction(datum["name"])
    opposite_direction = Direction(datum["opposite"])
    direction.opposite = opposite_direction
    opposite_direction.opposite = direction    
    directions.append(direction)
    directions.append(opposite_direction)

rooms = []
for datum in room_data:
    room = Room(datum["name"], datum["description"])
    rooms.append(room)

for datum in exit_data:
    from_name = datum["from"]
    to_name = datum["to"]
    direction_name = datum["direction"]
    if "one_way" in datum:
        one_way = datum["one_way"]
    else:
        one_way = False
    
    from_room = None
    to_room = None
    for room in rooms:
        if room.name == from_name:
            from_room = room
        elif room.name == to_name:
            to_room = room

    connected_rooms = [from_room, to_room]
    for connected_room in connected_rooms:
        if connected_room == None:
            print("Unknown room in connection between '" + from_name + "' and '" + to_name + "'")
            sys.exit()

    exit = None
    for direction in directions:
        if direction.name == direction_name:
            exit = direction
    if exit == None:
        print("Unknown direction '" + direction_name + "'")
        sys.exit()

    add_exit_func = None
    if one_way:
        add_exit_func = Room.add_one_way_exit
    else:
        add_exit_func = Room.add_exit
    add_exit_func(from_room, exit, to_room)

if len(rooms) > 0:
    game = Game(rooms[0])
    game.run()