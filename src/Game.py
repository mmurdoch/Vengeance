from __future__ import print_function

import sys

from Command import Command
from Player import Player


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