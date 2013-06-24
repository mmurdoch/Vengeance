"""
A game player.
"""


class _Player:
    """
    A player of a game.
    """
    def __init__(self, starting_location):
        """
        Creates a player.

        :param Location starting_location: The location in which the
        player starts
        """
        self._current_location = starting_location

    @property
    def current_location(self):
        """
        The current location in which the player resides.
        """
        return self._current_location

    def move_to(self, location):
        """
        Moves the player to a location.

        :param Location location: The location to which the player will move
        """
        self._current_location = location
