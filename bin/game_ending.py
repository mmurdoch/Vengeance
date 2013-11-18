# Use case: Ending a game when an appropriate state is reached
# Example: A randomly generated maze won when the user reaches the end
from vengeance.directions import NORTH, SOUTH, EAST, WEST
from vengeance.game import Direction
from vengeance.game import Game
from vengeance.game import Location

import random

# The maze is generated recursively, setting these values
# above 18 x 18 blows the stack!
width = 10
height = 10

def run_maze_game(maze):
    """
    Allows a user to move through a maze. They start at the bottom left
    (0, 0) and win when they reach the top right.
    """
    game = Game(locations_from_maze(maze))

    game.display_handler(render_maze(maze))

    # The function which determines whether the game ending
    # criteria have been met
    def check_if_end_reached(game):
        maze_end_location = maze[width-1][height-1]
        if game.character.current_location.name == maze_end_location.name:
            game.display_handler('You have reached the end. Well done!')
            game.should_end = True

    # Ensure that the game ending check happens at the end of
    # each iteration of the game loop
    game.end_of_round_handler = check_if_end_reached

    game.run()

def locations_from_maze(maze):
    locations = []
    for x in range(width):
        for y in range(height):
            locations.append(maze[x][y])

    return locations

def add_exits(x, y, maze, visited_locations):
    location = maze[x][y]

    allowed_location_coords = []
    if x in range(0, width-1) and not_visited(maze[x+1][y]):
        allowed_location_coords.append([x+1, y])

    if x in range(1, width) and not_visited(maze[x-1][y]):
        allowed_location_coords.append([x-1, y])

    if y in range(0, height-1) and not_visited(maze[x][y+1]):
        allowed_location_coords.append([x, y+1])

    if y in range(1, height) and not_visited(maze[x][y-1]):
        allowed_location_coords.append([x, y-1])

    exit_count = len(allowed_location_coords)
    if exit_count == 0:
        if can_backtrack(visited_locations):
            backtrack(maze, visited_locations)

        return

    visited_locations.append(location)
    location_coords = allowed_location_coords[random.randrange(exit_count)]

    new_x = location_coords[0]
    new_y = location_coords[1]
    new_location = maze[new_x][new_y]

    direction = None
    if new_x < x:
        direction = WEST
    elif new_x > x:
        direction = EAST
    elif new_y < y:
        direction = SOUTH
    else:
        direction = NORTH

    location.add_exit(direction, new_location)

    add_exits(new_x, new_y, maze, visited_locations)

def can_backtrack(visited_locations):
    return visited_locations

def backtrack(maze, visited_locations):
    previous_location = visited_locations.pop()
    for x in range(width):
        for y in range(height):
            current_location = maze[x][y]
            if previous_location.name == current_location.name:
                add_exits(x, y, maze, visited_locations)

def not_visited(location):
    return not location.exits

def render_maze(maze):
    result = ' ' + width * '_ '
    result += '\n'

    for y in range(height-1, -1, -1):
        result += '|'

        for x in range(width):
            location = maze[x][y]
            if y == 0 or has_wall_in_direction(location, SOUTH):
                result += '_'
            else:
                result += ' '

            if x == width-1 or has_wall_in_direction(location, EAST):
                result += '|'
            else:
                result += ' '

        result += '\n'

    return result

def has_wall_in_direction(location, direction):
    for exit in location.exits:
        if exit.direction.name == direction.name:
            return False

    return True

def random_coords():
    return random.randrange(width), random.randrange(height)

def create_maze():
    maze = []
    for x in range(width):
        locations_at_x = []
        maze.append(locations_at_x)
        for y in range(height):
            location = Location('Location '+str(x)+', '+str(y))
            locations_at_x.append(location)

    return maze

maze = create_maze()
starting_x, starting_y = random_coords()
visited_locations = []
add_exits(starting_x, starting_y, maze, visited_locations)

run_maze_game(maze)
