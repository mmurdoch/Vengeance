from __future__ import print_function
import readline
import curses

class Homestead:
    def __init__(self):
        self.stdscr = curses.initscr()
        curses.noecho()
        curses.cbreak()
        self.stdscr.keypad(1)

    def display(self, x, y, string):
        self.stdscr.addstr(y, x, string)
        self.stdscr.getch()

    def stop(self):
        curses.nocbreak()
        self.stdscr.keypad(0)
        curses.echo()
        curses.endwin()

print("Homestead")
print()
print("Waking from a deep and dreamless sleep, you slowly open your eyes")
print("and focus on the bright light set in the white ceiling over your head.")
print("Pulling yourself up, you sit on the edge of the bed and take stock")
print("of your surroundings.")
print("Apart from the bed the room is largely empty. There is a door in")
print("one corner of the room and a display screen embedded in one wall")

print("You are not authorized to unlock the door from this terminal")

while True:
    print("What now?")
    input = raw_input()
    if input == "open door":
        print("The door won't open, perhaps it is locked")
    elif input == "examine display":
        print("The display is dark, but as you run your fingers over its")
        print("surface it emits a faint glow and then this appears:")
        print()
        print(" |    Welcome to Homestead 9000")
        print(" | Your complete automation system")
        print(" | ")
        print(" | This is bedroom 3")
    elif input == "curses":
        homestead = Homestead()
        homestead.display(0, 0, "Hello world")
        homestead.stop()