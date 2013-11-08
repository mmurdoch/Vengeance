"""
Text adventure game engine.
"""
from __future__ import print_function


class _Command(object):
    """
    A command which can be given by a player.

    A command can be activated using its name or one of its synonyms.

    :param string name: The name of the command
    :param function func: The function to be called when the command
        is activated. This function must take two parameters, a
        PlayerCharacter and a context
    :param context: The context to be passed to func when it is called
    """
    def __init__(self, name, func, context):
        self._name = name
        self._synonyms = []
        self._func = func
        self._context = context

    @property
    def name(self):
        """
        The name of the command.

        :getter: Returns the name of the command
        :type: string
        """
        return self._name

    def add_synonym(self, synonym):
        """
        Adds a synonym for the command.

        :param string synonym: Alternative input which will activate
            the command
        """
        self._synonyms.append(synonym)

    def matches(self, value):
        """
        Returns whether or not an input value matches the command
        name or one of its synonyms.

        :param string value: The input value to check
        :return: True if the value matches this command, False otherwise
        :rtype: boolean
        """
        for synonym in self._synonyms:
            if synonym == value:
                return True

        return self.name == value

    def run(self, game):
        """
        Executes the command.

        :param Game game: The game for which to execute the command
        """
        self._func(game, self._context)


class Direction(object):
    """
    A direction in which movement can be made.

    :param string name: The unique name of the direction
    """
    def __init__(self, name):
        self._name = name
        self._opposite = None

    @property
    def name(self):
        """
        The name of the direction.

        :getter: Returns the direction's name
        :type: string
        """
        return self._name

    @property
    def opposite(self):
        """
        The opposite direction (as 'east' is to 'west',
        'in' is to 'out', etc.).

        :getter: Returns the direction's opposite direction
        :setter: Sets the opposite direction of the direction and
            also sets the direction as its opposite's opposite.
        :type: Direction
        """
        return self._opposite

    @opposite.setter
    def opposite(self, value):
        # Disable 'Access to a protected member _opposite of a client class'
        # pylint: disable=W0212
        """
        See opposite property.
        """
        self._opposite = value
        value._opposite = self


class Exit(object):
    """
    An exit from a location.

    :param Direction direction: The direction in which the exit resides
    :param Location to_location: The location to which the exit leads
    """
    def __init__(self, direction, to_location):
        self._direction = direction
        self._to_location = to_location

    @property
    def direction(self):
        """
        The direction in which the exit resides.

        :getter: Returns the exit direction
        :type: Direction
        """
        return self._direction

    @property
    def to_location(self):
        """
        The location to which the exit leads.

        :getter: Returns the exit location
        :type: Location
        """
        return self._to_location


class Game(object):
    """
    An adventure game.

    :param list locations: The locations in the game. The first location
        in the list is the one in which the player's character starts
    :raises: ``ValueError`` if locations does not contain at least one
        location
    """
    def __init__(self, locations):
        if not locations:
            raise ValueError('locations must contain at least one location')

        self._locations = locations
        self._character = PlayerCharacter(locations[0])
        self._commands = []
        quit_command = _Command('quit', Game._quit, self)
        quit_command.add_synonym('q')
        self._add_command(quit_command)
        self._handlers = {
            'display': _default_display_handler,
            'input': _default_input_handler,
            'location_renderer': _default_location_renderer,
            'quit': _default_quit_handler
        }
        self._should_quit = False

    @property
    def character(self):
        """
        The player's active character in the game.

        :getter: Returns the active character
        :type: PlayerCharacter
        """
        return self._character

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

    def _find_command(self, command_name):
        """
        Finds a command by name or synonym. The command is searched for
        within this game and the current location of the character.

        :param string command_name: The name or synonym of the command to find
        :return: the first matching command or None if not found
        :rtype: Command
        """
        found_commands = self._find_commands(command_name)
        if len(found_commands) == 1:
            return found_commands[0]

        return None

    def _find_commands(self, command_name):
        # Disable 'Access to a protected member _commands of a client class'
        # Disable 'Access to a protected member _current_location of
        # a client class'
        # pylint: disable=W0212
        """
        Finds all commands which match the specified name or synonym.
        Commands are searched for within this game and the current
        location of the character.

        :param string command_name: The name or synonym of the commands to
            find
        :return: all matching commands
        :rtype: list
        """
        found_commands = []

        for command in self._commands:
            if command.matches(command_name):
                found_commands.append(command)

        for command in self.character._current_location._commands:
            if command.matches(command_name):
                found_commands.append(command)

        return found_commands

    def _add_command(self, command):
        """
        Adds a command to the game.

        :param _Command command: Command to add
        """
        self._commands.append(command)

    def run(self):
        """
        Runs the game.
        """
        while (True):
            current_location = self.character.current_location
            rendered_location = self.location_renderer(current_location)
            self.display_handler(rendered_location)

            user_input = self.input_handler()
            self.process_input(user_input)

            if self._should_quit:
                break

    @property
    def display_handler(self):
        """
        The function to be called for the game to display some text. This
        function takes a single string parameter (the text to be displayed).

        :getter: Returns the current display handler
        :setter: Sets the function to be called when some text is to
            be displayed.
        :type: function
        """
        return self._handlers['display']

    @display_handler.setter
    def display_handler(self, value):
        """
        See display_handler property.
        """
        self._handlers['display'] = value

    @property
    def input_handler(self):
        """
        The function to be called for the game to get input from the user.
        This function takes no parameters and returns a string (the input).

        :getter: Returns the current input handler
        :setter: Sets the function to be called when input is required from
            the user.
        :type: function
        """
        return self._handlers['input']

    @input_handler.setter
    def input_handler(self, value):
        """
        See input_handler property.
        """
        self._handlers['input'] = value

    @property
    def location_renderer(self):
        """
        The function to be called when the game renders a location. This
        function takes a single Location parameter and returns a string
        representation of the location.

        :getter: Returns the current location renderer
        :setter: Sets the function to be called when a location is to
            be rendered.
        :type: function
        """
        return self._handlers['location_renderer']

    @location_renderer.setter
    def location_renderer(self, value):
        """
        See location_renderer property.
        """
        self._handlers['location_renderer'] = value

    @property
    def quit_handler(self):
        """
        The function to be called when the game is requested to quit. This
        function takes two parameters - a display_handler function (see
        display_handler property) and an input_handler function (see
        input_handler property) - and returns a bool which is True if the
        game should quit, or False otherwise.

        :getter: Returns the current quit handler
        :setter: Sets the function to be called when quit is
            requested.
        :type: function
        """
        return self._handlers['quit']

    @quit_handler.setter
    def quit_handler(self, value):
        """
        See quit_handler property.
        """
        self._handlers['quit'] = value

    def _move_character_to(self, location):
        """
        Moves the character to a location.

        :param Location location: The location to which to move the character
        """
        # Disable 'Access to a protected member _move_to of a client class'
        # pylint: disable=W0212
        self.character._move_to(location)

    def _quit(self, _):
        """
        Interacts with the user to determine whether to quit the game.

        :param _: The context in which the quit was initiated (ignored)
        """
        self._should_quit = self.quit_handler(
            self.display_handler, self.input_handler)

    def process_input(self, user_input):
        """
        Processes input from the user.

        :param string user_input: The input command to process
        """
        command = self._find_command(user_input)
        if command:
            command.run(self)


def _default_display_handler(text):
    """
    Displays text to the user.

    :param string text: The text to display
    """
    print(text)


def _default_input_handler():
    """
    Retrieves input from the user.
    """
    return raw_input()


def _default_location_renderer(location):
    """
    Converts a location to a default textual representation.

    :param Location location: The location to render
    :return: A textual representation of the location
    :rtype: string
    """
    title = location.name
    title += ' (exits: '
    exit_count = len(location.exits)
    if exit_count == 0:
        title += '<none>'
    for i in range(exit_count):
        an_exit = location.exits[i]
        title += an_exit.direction.name
        if i < exit_count - 1:
            title += ', '
    title += ')'
    if location.description:
        title += '\n'
        title += location.description
    return title


def _default_quit_handler(display_handler, input_handler):
    """
    Interacts with the user to determine whether to quit the game.

    :return: True if the game should be quit, False otherwise
    :param function display_handler: A function for displaying text to the
        user (see Game.display_handler)
    :param function input_handler: A function for retrieving input from mthe
        user (see Game.input_handler)
    :rtype: bool
    """
    display_handler("Are you sure you want to quit?")
    quit_input = input_handler()
    if quit_input == "y" or quit_input == "yes":
        return True

    return False


class GameFormatException(Exception):
    """
    Thrown when invalid game data is processed.
    """
    pass


class Location(object):
    """
    A location in an adventure game.

    :param string name: The unique name of the location
    :param string description: The description of the location
    """
    def __init__(self, name, description=''):
        self._commands = []
        self._exits = []
        self._name = name
        self._description = description

    def add_exit(self, direction, location):
        """
        Adds an exit from the location.

        The exit is two-way. It can be used both to move from
        the location to the connected location and also to move back.

        :param Direction direction: The direction in which the exit resides
        :param Location location: The location reached by going through
            the exit
        """
        self.add_one_way_exit(direction, location)
        location.add_one_way_exit(direction.opposite, self)

    def add_one_way_exit(self, direction, location):
        # Disable 'Access to a protected member _move_character_to of a
        # client class'
        # pylint: disable=W0212
        """
        Adds a one-way exit from the location.

        The exit can only be used to move from the location to the
        connected location. It does not allow movement back again.

        :param Direction direction: The direction in which the exit resides
        :param Location location: The location reached by going through
            the exit
        """
        self._exits.append(Exit(direction, location))
        exit_command = _Command(
            direction.name, Game._move_character_to, location)
        exit_command.add_synonym(direction.name[0])
        self._commands.append(exit_command)

    @property
    def name(self):
        """
        The name of the location.

        :getter: Returns the location name
        :type: string
        """
        return self._name

    @property
    def description(self):
        """
        The description of the location.

        :getter: Returns the location description
        :type: string
        """
        return self._description

    @property
    def exits(self):
        """
        The exits from the location.

        :getter: Returns the location exits
        :type: tuple of Exit objects
        """
        return tuple(self._exits)


class PlayerCharacter(object):
    # Disable 'Too few public methods'
    # pylint: disable=R0903
    """
    A character within a game controlled by a player.

    :param Location starting_location: The location in which the
        character starts
    """
    def __init__(self, starting_location):
        self._current_location = starting_location

    @property
    def current_location(self):
        """
        The current location in which the character resides.

        :getter: Returns the character's current location
        :type: Location
        """
        return self._current_location

    def _move_to(self, location):
        """
        Moves the character to a location.

        :param Location location: The location to which the character
            will move
        """
        self._current_location = location
