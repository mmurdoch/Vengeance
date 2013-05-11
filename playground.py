"""
A playground in which to try out text adventure ideas.
"""
from __future__ import print_function
import sys


class Room:
    """
    A room in an adventure game.
    """
    def __init__(self, name, description):
        """
        Creates a room.

        name: The unique name of the room
        description: The description of the room
        """
        self._commands = []
        self._exits = []
        self._name = name
        self._description = description

    def add_exit(self, direction, room):
        """
        Adds an exit from the room.

        The exit is two-way. It can be used both to move from
        the room to the connected room and also to move back.

        direction: The direction in which the exit resides
        room: The room reached by going through the exit
        """
        self.add_one_way_exit(direction, room)
        room.add_one_way_exit(direction.opposite, self)

    def add_one_way_exit(self, direction, room):
        """
        Adds a one-way exit from the room.

        The exit can only be used to move from the room to the
        connected room. It does not allow movement back again.

        direction: The direction in which the exit resides
        room: The room reached by going through the exit
        """
        self._exits.append(Exit(direction.name, room))
        exit_command = Command(direction.name, Game.move_player_to, room)
        exit_command.add_synonym(direction.name[0])
        self._commands.append(exit_command)

    @property
    def commands(self):
        """
        The commands that can be performed in the room.
        """
        return self._commands

    @property
    def exits(self):
        """
        The exits from the room.
        """
        return self._exits

    @property
    def name(self):
        """
        The unique name of the room.
        """
        return self._name

    @property
    def description(self):
        """
        The description of the room.
        """
        return self._description


class Exit:
    """
    An exit from a room.
    """
    def __init__(self, direction, to_room):
        self._direction = direction
        self._to_room = to_room

    @property
    def direction(self):
        """
        The direction in which the exit resides.
        """
        return self._direction

    @property
    def to_room(self):
        """
        The room to which the exit leads.
        """
        return self._to_room


class Command:
    """
    A command which can be given by a user.

    A command can be activated using its name or one of its synonyms.
    """
    def __init__(self, name, func, context):
        """
        Creates a command.

        name: The name of the command
        func: The function to be called when the command is activated
        context: The context to be passed to func when it is called
        """
        self._name = name
        self._synonyms = []
        self._func = func
        self._context = context

    @property
    def name(self):
        """
        The name of the command.
        """
        return self._name

    def add_synonym(self, synonym):
        """
        Adds a synonym for the command.

        synonym: Alternative input which will activate the command
        """
        self._synonyms.append(synonym)

    def matches(self, value):
        """
        Returns whether or not an input value matches the command
        name or one of its synonyms.

        value: The input value to check
        """
        for synonym in self._synonyms:
            if synonym == value:
                return True

        return self.name == value

    def run(self, player):
        """
        Executes the command.

        player: The player for which to execute the command
        """
        self._func(player, self._context)


class Player:
    """
    A player of a game.
    """
    def __init__(self, starting_room):
        """
        Creates a player.

        starting_room: The room in which the player starts
        """
        self._current_room = starting_room

    @property
    def current_room(self):
        """
        The current room in which the player resides.
        """
        return self._current_room

    def move_to(self, room):
        """
        Moves the player to a room.

        room: The room to which the player will move
        """
        self._current_room = room


class Game:
    """
    An adventure game.
    """
    def __init__(self, starting_room):
        """
        Creates a game.

        starting_room: The room in which the player will start
        """
        self._player = Player(starting_room)
        self._commands = []
        self.add_command(Command("quit", Game.quit, self))

    def add_command(self, command):
        """
        Adds a command to the game.

        command: Command to add
        """
        self._commands.append(command)

    def run(self):
        """
        Runs the game.
        """
        while (True):
            display_room(self._player.current_room)
            self._process_command(get_input())

    def move_player_to(self, room):
        """
        Moves the player to a room.

        room: The room to which to move the player
        """
        self._player.move_to(room)

    def quit(self, _):
        """
        Interacts with the user to determine whether to quit the game.

        context: The context in which the quit was initiated
        """
        print("Are you sure you want to quit?")
        quit_input = get_input()
        if quit_input == "y" or quit_input == "yes":
            self.save()
            sys.exit()

    def save(self):
        """
        Saves the game.
        """
        pass

    def _process_command(self, user_input):
        """
        Processes a command from the user.

        user_input: The input command to process
        """
        for command in self._commands:
            if command.matches(user_input):
                command.run(self)

        room = self._player.current_room
        for command in room.commands:
            if command.matches(user_input):
                command.run(self)


class Direction:
    """
    A direction in which movement can be made.
    """
    def __init__(self, name):
        """
        Creates a direction.

        name: The unique name of the direction
        """
        self._name = name
        self._opposite = None

    @property
    def name(self):
        """
        The unique name of the direction.
        """
        return self._name

    @property
    def opposite(self):
        """
        The opposite direction (as 'east' is to 'west',
        'in' is to 'out', etc.)
        """
        return self._opposite

    @opposite.setter
    def opposite(self, value):
        """
        Sets the opposite direction.
        """
        self._opposite = value


def display_room(room):
    """
    Displays room information to the user.

    room: The room for which to display information
    """
    title = room.name
    title += " (exits: "
    if len(room.exits) == 0:
        title += "<none> "
    for an_exit in room.exits:
        title += an_exit.direction
        title += " "
    title += "\b"
    title += ")"
    print(title)
    print(room.description)


def get_input():
    """
    Retrieves input from the user.
    """
    return raw_input()


def create_directions(direction_data):
    """
    Creates the directions in the game.

    direction_data: Details of the directions in the game
    """
    directions = []
    for datum in direction_data:
        direction = Direction(datum["name"])
        opposite_direction = Direction(datum["opposite"])
        direction.opposite = opposite_direction
        opposite_direction.opposite = direction
        directions.append(direction)
        directions.append(opposite_direction)

    return directions


def create_rooms(room_data):
    """
    Creates the rooms in the game.

    room_data: Details of the rooms in the game
    """
    rooms = []
    for room_datum in room_data:
        room_name = room_datum['name']
        room = Room(room_name, room_datum['description'])
        rooms.append(room)

    return rooms


def create_exit_data(room_data):
    """
    Creates exit data for the game.

    room_data: Details of the rooms in the game
    """
    exit_data = []
    for room_datum in room_data:
        room_name = room_datum['name']
        room_datum.setdefault('exits', [])
        for current_exit in room_datum['exits']:
            exit_datum = {
                'from': room_name,
                'to': current_exit['to'],
                'direction': current_exit['direction']
            }
            exit_data.append(exit_datum)

    return exit_data


def find_room(name, rooms):
    """
    Finds a room by name.

    Returns the room or None if the room was not found.

    name: The name of the room to find
    rooms: The rooms in which to search
    """
    for room in rooms:
        if room.name == name:
            return room

    return None


def add_exits(rooms, directions, exit_data):
    """
    Adds exits to rooms.

    rooms: The rooms to which to add exits
    directions: The directions in which exits can lead
    exit_data: Details of the exits in the game
    """
    for datum in exit_data:
        from_name = datum["from"]
        from_room = find_room(from_name, rooms)
        to_name = datum["to"]
        to_room = find_room(to_name, rooms)
        if to_room is None:
            print("Unknown exit room '" + to_name +
                  "' from '" + from_name + "'")
            sys.exit()

        direction_name = datum["direction"]
        the_exit = None
        for direction in directions:
            if direction.name == direction_name:
                the_exit = direction
        if the_exit is None:
            print("Unknown direction '" + direction_name + "'")
            sys.exit()

        datum.setdefault('one_way', False)
        one_way = datum["one_way"]
        add_exit_func = None
        if one_way:
            add_exit_func = Room.add_one_way_exit
        else:
            add_exit_func = Room.add_exit
        add_exit_func(from_room, the_exit, to_room)


def run_game(game_data):
    """
    Runs the game.

    game_data: Details of the rooms in the game
    """
    directions = create_directions(game_data['directions'])
    room_data = game_data['rooms']
    rooms = create_rooms(room_data)
    exit_data = create_exit_data(room_data)
    add_exits(rooms, directions, exit_data)

    if len(rooms) > 0:
        game = Game(rooms[0])
        game.run()

run_game({
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
