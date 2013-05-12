class Command:
    """
    A command which can be given by a user.

    A command can be activated using its name or one of its synonyms.
    """
    def __init__(self, name, func, context):
        """
        Creates a command.

        name: The name of the command
        func: The function to be called when the command is activated
        context: The context to be passed to func when it is called
        """
        self._name = name
        self._synonyms = []
        self._func = func
        self._context = context

    @property
    def name(self):
        """
        The name of the command.
        """
        return self._name

    def add_synonym(self, synonym):
        """
        Adds a synonym for the command.

        synonym: Alternative input which will activate the command
        """
        self._synonyms.append(synonym)

    def matches(self, value):
        """
        Returns whether or not an input value matches the command
        name or one of its synonyms.

        value: The input value to check
        """
        for synonym in self._synonyms:
            if synonym == value:
                return True

        return self.name == value

    def run(self, player):
        """
        Executes the command.

        player: The player for which to execute the command
        """
        self._func(player, self._context)
