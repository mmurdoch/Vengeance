"""
Text adventure game engine.
"""
from __future__ import print_function

import sys

from vengeance._command import _Command
from vengeance._exit import _Exit
from vengeance._player import _Player


class Game:
    # Disable 'Too few public methods'
    # pylint: disable=R0903
    """
    An adventure game.
    """
    def __init__(self, locations):
        """
        Creates a game.

        :param list locations: The locations in the game. The first location
        in the list is the one in which the character starts
        """
        self._locations = locations
        self._player = _Player(locations[0])
        self._commands = []
        self._add_command(_Command("quit", Game._quit, self))

    def _add_command(self, command):
        """
        Adds a command to the game.

        command: Command to add
        """
        self._commands.append(command)

    def _run(self):
        """
        Runs the game.
        """
        while (True):
            _display_location(self._player.current_location)
            self._process_command(_get_input())

    def _move_player_to(self, location):
        """
        Moves the player to a location.

        :param Location location: The location to which to move the player
        """
        self._player.move_to(location)

    def find_location(self, location_name):
        """
        Finds a location by name.

        :param string location_name: The name of the location to find
        :return: the found location or None if the location was not found
        :rtype: Location
        """
        for location in self._locations:
            if location.name == location_name:
                return location

        return None

    def _quit(self, _):
        """
        Interacts with the user to determine whether to quit the game.

        context: The context in which the quit was initiated
        """
        print("Are you sure you want to quit?")
        quit_input = _get_input()
        if quit_input == "y" or quit_input == "yes":
            self._save()
            sys.exit()

    def _save(self):
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

        room = self._player.current_location
        for command in room.commands:
            if command.matches(user_input):
                command.run(self)


def _display_location(location):
    """
    Displays location information to the user.

    :param Location location: The location for which to display information
    """
    title = location.name
    title += " (exits: "
    if len(location.exits) == 0:
        title += "<none> "
    for an_exit in location.exits:
        title += an_exit.direction
        title += " "
    title += "\b"
    title += ")"
    print(title)
    print(location.description)


def _get_input():
    """
    Retrieves input from the user.
    """
    return raw_input()


class Location:
    # Disable 'Too few public methods'
    # pylint: disable=R0903
    """
    A location in an adventure game.
    """
    def __init__(self, name, description):
        """
        Creates a location.

        :param string name: The unique name of the location
        :param string description: The description of the location
        """
        self._commands = []
        self._exits = []
        self._name = name
        self._description = description

    def _add_exit(self, direction, location):
        # Disable 'Access to a protected member _run of a client class'
        # pylint: disable=W0212
        """
        Adds an exit from the location.

        The exit is two-way. It can be used both to move from
        the location to the connected location and also to move back.

        :param direction: The direction in which the exit resides
        :param Location location: The location reached by going through
        the exit
        """
        self._add_one_way_exit(direction, location)
        location._add_one_way_exit(direction.opposite, self)

    def _add_one_way_exit(self, direction, location):
        # Disable 'Access to a protected member _run of a client class'
        # pylint: disable=W0212
        """
        Adds a one-way exit from the location.

        The exit can only be used to move from the location to the
        connected location. It does not allow movement back again.

        :param direction: The direction in which the exit resides
        :param Location location: The location reached by going through
        the exit
        """
        self._exits.append(_Exit(direction.name, location))
        exit_command = _Command(
            direction.name, Game._move_player_to, location)
        exit_command.add_synonym(direction.name[0])
        self._commands.append(exit_command)

    @property
    def name(self):
        """
        The unique name of the location.
        """
        return self._name

    @property
    def description(self):
        """
        The description of the location.
        """
        return self._description

    @property
    def exits(self):
        """
        The exits from the location.
        """
        return self._exits


class GameFormatException(Exception):
    """
    Thrown when invalid game data is processed.
    """
    pass
