class _Exit:
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
