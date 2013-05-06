from __future__ import print_function
import sys

class Room:
    def __init__(self, name, description):
        self.exits = []
        self.name = name
        self.description = description
        
    def add_exit(self, exit):
        self.exits.append(exit)
        
    def __str__(self):
        string = self.name
        string += ":\n"
        string += "Exits:\n"
        if (len(self.exits) == 0):
            string += "[None]"
        else:
            for exit in self.exits:
                string += exit.name
       
        return string

class Exit:
    def __init__(self, direction, to_room):
        self.direction = direction
        self.to_room = to_room

class Command:
    def __init__(self, name, func):
        self._name = name
        self._func = func
    
    @property
    def name(self):
        return self._name

    def run(self):
        self._func()

class Player:
    def __init__(self, current_room):
        self.move_to(current_room)

    @property
    def current_room(self):
        return self._current_room
    
    def move_to(self, room):
        self._current_room = room

class Game:
    def __init__(self, starting_room):
        self.starting_room = starting_room
        self.commands = []

    def add_command(self, command):
        self.commands.append(command)

    def run(self):
        player = Player(self.starting_room)
        while (True):
            self.display_room(player.current_room)
            user_input = self.get_input()
            for command in self.commands:
                if user_input == command.name:
                    command.run()
            room = player.current_room
            for exit in room.exits:
                if user_input == exit.direction:
                    player.move_to(exit.to_room)

    def display_room(self, room):
        title = room.name
        title += " (exits: "
        if len(room.exits) == 0:
            title += "<none>"
        for exit in room.exits:
            title += exit.direction
            title += " "
        title += "\b"
        title += ")"
        print(title)
        print(room.description)

    def get_input(self):
        return raw_input()

hole = Room("Hole", "A wet, dirty great pit in the ground")
big_dusty_field = Room("Big Dusty Field", 
    "Has the distinct odour of dried-up cow pats...")
the_void = Room("The Void", "An empty space, devoid of life")

hole.add_exit(Exit("up", big_dusty_field))
big_dusty_field.add_exit(Exit("down", hole))
big_dusty_field.add_exit(Exit("up", the_void))

game = Game(hole)

def quit_game():
    print("Are you sure you want to quit?")
    quit_input = raw_input()
    if quit_input == "y" or quit_input == "yes":
        sys.exit()

game.add_command(Command("quit", quit_game))
game.run()
