# Use case: A randomly generated maze won when the user reaches the end
# Example:
from vengeance.game import Direction
from vengeance.game import Game
from vengeance.game import Location

import random

# The maze is generated recursively, setting these values
# above 18 x 18 blows the stack
width = 10
height = 10

north = Direction('north')
south = Direction('south')
north.opposite = south

east = Direction('east')
west = Direction('west')
east.opposite = west

def set_exits(x, y, location_grid, visited_locations):
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

    exit_count = len(allowed_location_coords)
    if exit_count == 0:
        if backtracking(visited_locations):
            backtrack(location_grid, visited_locations)

        return

    visited_locations.append(location)
    location_coords = allowed_location_coords[random.randrange(exit_count)]

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

    set_exits(new_x, new_y, location_grid, visited_locations)

def backtracking(visited_locations):
    return visited_locations

def backtrack(location_grid, visited_locations):
    previous_location = visited_locations.pop()
    for i in range(width):
        for j in range(height):
            current_location = location_grid[i][j]
            if previous_location.name == current_location.name:
                set_exits(i, j, location_grid, visited_locations)

def not_visited(location):
    return not location.exits

def render_maze(location_grid):
    result = ' ' + width * '_ '
    result += '\n'

    for y in range(height-1, -1, -1):
        result += '|'

        for x in range(width):
            location = location_grid[x][y]
            if y == 0 or has_south_wall(location):
                result += '_'
            else:
                result += ' '

            if x == width-1 or has_east_wall(location):
                result += '|'
            else:
                result += ' '

        result += '\n'

    return result

def has_south_wall(location):
    for exit in location.exits:
        if exit.direction.name == south.name:
            return False

    return True

def has_east_wall(location):
    for exit in location.exits:
        if exit.direction.name == east.name:
            return False

    return True

def random_coords():
    return random.randrange(width), random.randrange(height)

# Create maze (a grid of locations)
location_grid = []
for x in range(width):
    locations_at_x = []
    location_grid.append(locations_at_x)
    for y in range(height):
        locations_at_x.append(Location('' + str(x) + ', ' + str(y)))

# Pick a random starting location
starting_x, starting_y = random_coords()

visited_locations = []
set_exits(starting_x, starting_y, location_grid, visited_locations)

print(render_maze(location_grid))

locations = []
for x in range(width):
    for y in range(height):
        locations.append(location_grid[x][y])

game = Game(locations)

game.run()