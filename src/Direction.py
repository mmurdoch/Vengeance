class Direction:
    """
    A direction in which movement can be made.
    """
    def __init__(self, name):
        """
        Creates a direction.

        name: The unique name of the direction
        """
        self._name = name
        self._opposite = None

    @property
    def name(self):
        """
        The unique name of the direction.
        """
        return self._name

    @property
    def opposite(self):
        """
        The opposite direction (as 'east' is to 'west',
        'in' is to 'out', etc.)
        """
        return self._opposite

    @opposite.setter
    def opposite(self, value):
        """
        Sets the opposite direction.
        """
        self._opposite = value