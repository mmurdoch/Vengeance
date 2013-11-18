# Use case: Run a procedurally defined game
# Example:
from vengeance.directions import DOWN, IN, WEST
from vengeance.game import Direction
from vengeance.game import Game
from vengeance.game import Location

church = Location('A Church', 'Tiny place of worship')
crypt = Location('The Crypt', 'Dusty tomb filled with empty sarcophagi')
coffin = Location('A Coffin', 'A tight squeeze and pitch dark')
cave = Location('A Cave')

church.add_exit(DOWN, crypt)
crypt.add_one_way_exit(IN, coffin)
crypt.add_exit(WEST, cave)

game = Game([church, crypt, coffin, cave])

game.run()
