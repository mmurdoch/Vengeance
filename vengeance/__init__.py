"""
Vengeance - text adventure game engine.
"""
from vengeance.game import Direction
from vengeance.game import Game
from vengeance.game import GameFormatException
from vengeance.game import Location


class _Struct:
    # Disable 'Too few public methods'
    # pylint: disable=R0903
    """
    A structure based on a dictionary.
    """
    def __init__(self, **entries):
        """
        :param self: The instance to initialize
        :param entries: The dictionary entries to be accessed
        """
        self.__dict__.update(entries)


def _direction_name_key():
    """
    :returns: The dictionary key for a direction name
    """
    return 'name'


def _direction_opposite_key():
    """
    :returns: The dictionary key for a direction opposite
    """
    return 'opposite'


def _create_directions(direction_data):
    """
    Creates the directions in the game.

    direction_data: Details of the directions in the game
    """
    directions = []
    for datum in direction_data:
        _check_direction_well_formed(datum)

        # Disable 'Used * or ** magic
        # pylint: disable=W0142
        direction = _Struct(**datum)
        direction_names = [d.name for d in directions]
        _check_direction_valid(direction, direction_names)

        # Disable 'Instance of '_Struct' has no 'name' member
        # Disable 'Instance of '_Struct' has no 'opposite' member
        # pylint: disable=E1101
        name = direction.name
        opposite = direction.opposite

        reserved_word = 'quit'
        name_key = _direction_name_key()
        _check_if_direction_is_reserved(reserved_word, name, name_key)
        opposite_key = _direction_opposite_key()
        _check_if_direction_is_reserved(reserved_word, opposite, opposite_key)

        direction = Direction(name)
        opposite_direction = Direction(opposite)
        direction.opposite = opposite_direction
        opposite_direction.opposite = direction
        directions.append(direction)
        directions.append(opposite_direction)

    return directions


def _check_direction_well_formed(direction):
    """
    Checks the structure of a direction dictionary.

    :param dict direction: The direction to check
    :raises: ``GameFormatException`` if direction structure is invalid
    """
    name_key = _direction_name_key()
    opposite_key = _direction_opposite_key()

    if name_key not in direction:
        if opposite_key not in direction:
            message = u'Missing name and opposite from direction'
            raise GameFormatException(message)
        else:
            message = u'Missing name from direction with opposite "{0}"'
            raise GameFormatException(message.format(direction[opposite_key]))
    elif opposite_key not in direction:
        message = u'Missing opposite from direction with name "{0}"'
        raise GameFormatException(message.format(direction[name_key]))


def _check_direction_valid(direction, direction_names):
    """
    Checks the validity of a direction dictionary.

    :param dict direction: The direction to check
    :param list direction_names: The current set of direction names
    """
    if not isinstance(direction.name, str):
        raise GameFormatException(u'Direction name must be a string')

    if not isinstance(direction.opposite, str):
        raise GameFormatException(u'Direction opposite must be a string')

    if direction.name == direction.opposite:
        message = u'Direction "{0}" cannot be its own opposite'
        raise GameFormatException(message.format(direction.name))

    if direction.name in direction_names:
        message = u'Redefinition of direction "{0}"'
        raise GameFormatException(message.format(direction.name))

    if direction.opposite in direction_names:
        message = u'Redefinition of direction "{0}" as an opposite'
        raise GameFormatException(message.format(direction.opposite))


def _check_if_direction_is_reserved(reserved_word, to_check, to_check_key):
    """
    Checks if a direction is using a reserved word.

    :param str reserved_word: The reserved word to check
    :param str to_check: The direction to check
    :param str to_check_key: The direction dictionary key of ``to_check``
    :raises: ``GameFormatException`` if direction is using a reserved word
    """
    if to_check == reserved_word:
        message = u'Direction {0} cannot use reserved word "{1}"'
        raise GameFormatException(message.format(to_check_key, reserved_word))


def _create_rooms(room_data):
    """
    Creates the rooms in the game.

    :param list room_data: Details of the rooms in the game
    :returns: Created rooms
    :rtype: list of rooms
    """
    rooms = []
    for room_datum in room_data:
        if 'name' not in room_datum:
            if 'description' not in room_datum:
                message = u'Missing name and description from room'
                raise GameFormatException(message)
            else:
                description = room_datum['description']
                message = u'Missing name from room with description "{0}"'
                raise GameFormatException(message.format(description))

        name = room_datum['name']

        if 'description' not in room_datum:
            message = u'Missing description from room with name "{0}"'
            raise GameFormatException(message.format(name))

        if not isinstance(name, str):
            raise GameFormatException(u'Room name must be a string')

        if name in [r.name for r in rooms]:
            message = u'Redefinition of room "{0}"'
            raise GameFormatException(message.format(name))

        description = room_datum['description']
        if not isinstance(description, str):
            raise GameFormatException(u'Room description must be a string')

        room = Location(name, description)
        rooms.append(room)

    return rooms


def _create_exit_data(room_data):
    """
    Creates exit data for the game.

    room_data: Details of the rooms in the game
    """
    exit_data = []
    for room_datum in room_data:
        room_name = room_datum['name']
        room_datum.setdefault('exits', [])
        for current_exit in room_datum['exits']:
            current_exit.setdefault('one_way', False)

            if 'to' not in current_exit:
                if 'direction' not in current_exit:
                    if 'direction' not in current_exit:
                        message = u'Missing to room and direction from ' \
                                  u'exit from room "{0}"'
                        raise GameFormatException(message.format(room_name))
                else:
                    message = u'Missing to room from exit with direction ' \
                              u'"{0}" from room "{1}"'
                    raise GameFormatException(
                        message.format(current_exit['direction'], room_name))

            if 'direction' not in current_exit:
                message = u'Missing direction from exit to room "{0}" ' \
                          u'from room "{1}"'
                raise GameFormatException(
                    message.format(current_exit['to'], room_name))

            to_room = current_exit['to']
            if not isinstance(to_room, str):
                raise GameFormatException('Exit to room must be a string')

            direction = current_exit['direction']
            if not isinstance(direction, str):
                raise GameFormatException('Exit direction must be a string')

            one_way = current_exit['one_way']
            if not isinstance(one_way, bool):
                raise GameFormatException('Exit one_way must be a boolean')

            exit_datum = {
                'from': room_name,
                'to': to_room,
                'direction': direction,
                'one_way': one_way
            }
            exit_data.append(exit_datum)

    return exit_data


def _add_exits(game, directions, exit_data):
    """
    Adds exits to locations.

    game: The game containing the locations to which to add exits
    directions: The directions in which exits can lead
    exit_data: Details of the exits in the game
    """
    for datum in exit_data:
        from_name = datum['from']
        from_location = game.find_location(from_name)
        to_name = datum['to']
        to_location = game.find_location(to_name)
        if to_location is None:
            message = u'Unknown exit room "{0}" from "{1}"'
            raise GameFormatException(message.format(to_name, from_name))

        direction_name = datum['direction']
        the_exit = None
        for direction in directions:
            if direction.name == direction_name:
                the_exit = direction
        if the_exit is None:
            message = u'Unknown exit direction "{0}" from room "{1}"'
            raise GameFormatException(
                message.format(direction_name, from_name))

        one_way = datum['one_way']
        add_exit_func = None
        if one_way:
            add_exit_func = Location.add_one_way_exit
        else:
            add_exit_func = Location.add_exit
        add_exit_func(from_location, the_exit, to_location)


def _get_room_data(game_data):
    """
    Retrieves room data.

    :param dict game_data: Details of the rooms in the game (see run_game)
    :raises: GameFormatException if room data is invalid
    """
    if 'rooms' not in game_data:
        raise GameFormatException(u'Missing rooms list')

    room_data = game_data['rooms']

    if len(room_data) == 0:
        message = u'Rooms list must contain at least one room'
        raise GameFormatException(message)

    return room_data


def create_game(game_data):
    """
    Creates a game.

    :param dict game_data: Details of the game (see run_game)
    :returns: Created game or None if ``game_data`` contains no rooms
    :rtype: Game
    :raises: GameFormatException if ``game_data`` is invalid
    """
    if not isinstance(game_data, dict):
        raise GameFormatException(u'game_data must be a dictionary')

    if 'directions' not in game_data:
        raise GameFormatException(u'Missing directions list')

    directions = _create_directions(game_data['directions'])

    rooms = _create_rooms(_get_room_data(game_data))
    if len(rooms) > 0:
        game = Game(rooms)
        exit_data = _create_exit_data(_get_room_data(game_data))
        _add_exits(game, directions, exit_data)

        return game


def run_game(game_data):
    """
    Runs a game.

    :param dict game_data: Details of the game
    :raises: ``GameFormatException`` if ``game_data`` is invalid

    ``game_data`` is a dictionary containing two key-value pairs, one with key
    ``'directions'`` and the other with key ``'rooms'``. Each of these keys
    has a list as its value.

    The ``'directions'`` list contains a sequence of dictionaries, each with
    two key-value pairs: one with key ``'name'`` and the other with key
    ``'opposite'``. The values of each key are strings which the player can
    type to move in that direction. All direction ``'name'`` and
    ``'opposite'`` values must be unique.

    The ``'rooms'`` list also contains a sequence of dictionaries. Each of
    these dictionaries must contain a ``'name'`` key with a string value. No
    two rooms can have the same name. Each dictionary must also contain a
    ``'description'`` key which again must have a string value. In addition,
    each dictionary may optionally contain an ``'exits'`` key.

    The value of the ``'exits'`` key is (again!) a list of dictionaries which
    contain a ``'to'`` key (the value of which must be the ``'name'`` of a
    room) and a ``'direction'`` key (the value of which must contain the
    ``'name'`` or ``'opposite'`` of a direction). Also, optionally, each
    dictionary may contain a ``'one_way'`` key, the value of which must be a
    boolean (if ``True`` the exit can only be traversed from the location, not
    back again). The default is ``False``.

    Phew! An example might help::

        vengeance.run_game({
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

    """
    game = create_game(game_data)
    game.run()
