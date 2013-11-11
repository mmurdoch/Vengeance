# Use case: A randomly generated maze won when the user reaches the end
# Example:
from vengeance.game import Game
from vengeance.game import Location

import random

width = 4
height = 4

def set_exits(x, y, location_grid, visited_locations):
    location = location_grid[x][y]

    visited_locations.append(starting_location)

    # Get allowed directions from location
    allowed_directions = []
    if x == 0 and y == 0:
        allowed_directions = ['north', 'east']
    elif x == 0:
        # TODO TODO TODO
    # Pick a random direction (if any)
    # Knock a hole to next location

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

visited_locations = []
set_exits(starting_x, starting_y, location_grid, visited_locations)

locations = []
for x in range(width):
    for y in range(height):
        locations.append(location_grid[x][y])

game = Game(locations)

game.run()