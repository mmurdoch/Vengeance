# Use case: Embed the game engine
# Example:
import vengeance

# Use declaratively defined game but could just as easily be
# created procedurally
game = vengeance.create_game({
    'directions': [
        {'name': 'up', 'opposite': 'down'},
        {'name': 'in', 'opposite': 'out'},
        {'name': 'west', 'opposite': 'east'}
    ],
    'rooms': [
        {'name': 'A Church',
         'description': 'Tiny place of worship',
         'exits': [
             {'to': 'The Crypt', 'direction': 'down'}
         ]},
        {'name': 'The Crypt',
         'description': 'Dusty tomb filled with empty sarcophagi',
         'exits': [
             {'to': 'A Coffin', 'direction': 'in', 'one_way': True},
             {'to': 'A Cave', 'direction': 'west'}
         ]},
        {'name': 'A Coffin',
         'description': 'A tight squeeze and pitch dark'},
        {'name': 'A Cave',
         'description': 'A dark and dingy place'}
    ],
})

# Add a prompt to indicate when the game is waiting for user input
def prompt_for_input():
    return raw_input('> ')

game.input_handler = prompt_for_input

# Prepend all game generated information with a colon
def display_handler(text):
    print(': ' + text.replace('\n', '\n: '))

game.display_handler = display_handler

# Display the name of the location followed by the description
# without detailing the exits
def location_renderer(location):
    return location.name + ' - ' + location.description

game.location_renderer = location_renderer

# Don't ask the user for confirmation if they ask to quit the game
def quit_without_confirmation(display_handler, input_handler):
    return True

game.quit_handler = quit_without_confirmation

game.run()