class _Player:
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
