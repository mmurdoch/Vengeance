from vengeance.game import Direction
from vengeance.game import Game
from vengeance.game import Location

go_up = Direction('up')
go_down = Direction('down')
go_up.opposite = go_down

go_in = Direction('in')
go_out = Direction('out')
go_in.opposite = go_out

go_west = Direction('west')
go_east = Direction('east')
go_west.opposite = go_east

church = Location('A Church', 'Tiny place of worship')
crypt = Location('The Crypt', 'Dusty tomb filled with empty sarcophagi')
coffin = Location('A Coffin', 'A tight squeeze and pitch dark')
cave = Location('A Cave')

church.add_exit(go_down, crypt)
crypt.add_one_way_exit(go_in, coffin)
crypt.add_exit(go_west, cave)

game = Game([church, crypt, coffin, cave])
game._run()