"""
Common directions.
"""
from vengeance.game import Direction


class _DirectionPair(object):
    """
    A pair of directions, each of which is the opposite of the other.

    :param string direction_name: The name of one direction
    :param string opposite_name: The name of the other direction
    """
    def __init__(self, direction_name, opposite_name):
        direction = Direction(direction_name)
        opposite = Direction(opposite_name)
        direction.opposite = opposite
        self._direction = direction

    @property
    def direction(self):
        """
        One direction.

        :getter: Returns the direction
        :type: Direction
        """
        return self._direction

    @property
    def opposite(self):
        """
        The other direction.

        :getter: Returns the opposite direction
        :type: Direction
        """
        return self._direction.opposite


_NORTH_SOUTH = _DirectionPair('north', 'south')
_EAST_WEST = _DirectionPair('east', 'west')
_UP_DOWN = _DirectionPair('up', 'down')
_IN_OUT = _DirectionPair('in', 'out')

#: North (opposite: SOUTH).
NORTH = _NORTH_SOUTH.direction

#: South (opposite: NORTH).
SOUTH = _NORTH_SOUTH.opposite

#: East (opposite: WEST).
EAST = _EAST_WEST.direction

#: West (opposite: EAST).
WEST = _EAST_WEST.opposite

#: Up (opposite: DOWN).
UP = _UP_DOWN.direction

#: Down (opposite: UP).
DOWN = _UP_DOWN.opposite

#: In (opposite: OUT).
IN = _IN_OUT.direction

#: Out (opposite: IN).
OUT = _IN_OUT.opposite
