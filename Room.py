from Command import Command
from Exit import Exit
from Game import Game


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
