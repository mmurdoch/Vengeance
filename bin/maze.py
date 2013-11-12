# Use case: A randomly generated maze won when the user reaches the end
# Example:
from vengeance.game import Direction
from vengeance.game import Game
from vengeance.game import Location

import random

width = 4
height = 4
north = Direction('north')
south = Direction('south')
north.opposite = south
east = Direction('east')
west = Direction('west')
east.opposite = west

def set_exits(x, y, location_grid):
    location = location_grid[x][y]

    allowed_location_coords = []
    if x in range(0, width-1) and not_visited(location_grid[x+1][y]):
        allowed_location_coords.append([x+1, y])

    if x in range(1, width) and not_visited(location_grid[x-1][y]):
        allowed_location_coords.append([x-1, y])

    if y in range(0, height-1) and not_visited(location_grid[x][y+1]):
        allowed_location_coords.append([x, y+1])

    if y in range(1, height) and not_visited(location_grid[x][y-1]):
        allowed_location_coords.append([x, y-1])

    count = len(allowed_location_coords)
    if count == 0:
        return

    location_coords = allowed_location_coords[random.randrange(count)]

    new_x = location_coords[0]
    new_y = location_coords[1]
    new_location = location_grid[new_x][new_y]

    direction = None
    if new_x < x:
        direction = west
    elif new_x > x:
        direction = east
    elif new_y < y:
        direction = south
    else:
        direction = north

    location.add_exit(direction, new_location)

    set_exits(new_x, new_y, location_grid)

def not_visited(location):
    return not location.exits

# Create maze (a grid of locations)
location_grid = []
for x in range(width):
    locations_at_x = []
    location_grid.append(locations_at_x)
    for y in range(height):
        locations_at_x.append(Location('' + str(x) + ', ' + str(y)))

# Pick a random starting location
starting_x = random.randrange(width)
starting_y = random.randrange(height)

set_exits(starting_x, starting_y, location_grid)

locations = []
for x in range(width):
    for y in range(height):
        locations.append(location_grid[x][y])

game = Game(locations)

game.run()