"""
An adventure game.
"""
from __future__ import print_function

import sys

from vengeance._command import _Command
from vengeance._player import _Player


class _Game:
    """
    An adventure game.
    """
    def __init__(self, rooms):
        """
        Creates a game.

        starting_room: The room in which the player will start
        """
        self._rooms = rooms
        self._player = _Player(rooms[0])
        self._commands = []
        self.add_command(_Command("quit", _Game.quit, self))

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
            _display_room(self._player.current_room)
            self._process_command(_get_input())

    def move_player_to(self, room):
        """
        Moves the player to a room.

        room: The room to which to move the player
        """
        self._player.move_to(room)

    def find_room(self, room_name):
        """
        Finds a room by name.

        Returns the room or None if the room was not found.

        name: The name of the room to find
        rooms: The rooms in which to search
        """
        for room in self._rooms:
            if room.name == room_name:
                return room

        return None

    def quit(self, _):
        """
        Interacts with the user to determine whether to quit the game.

        context: The context in which the quit was initiated
        """
        print("Are you sure you want to quit?")
        quit_input = _get_input()
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


def _display_room(room):
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


def _get_input():
    """
    Retrieves input from the user.
    """
    return raw_input()
