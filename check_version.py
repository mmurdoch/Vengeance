import re
import sys

changes_file = open('CHANGES.txt', 'r')
changes_first_line = changes_file.readline()
changes_version = re.match(r'v(\d\.\d\.\d).*', changes_first_line).group(1)

setup_file = open('setup.py', 'r')
setup_content = setup_file.read()
setup_version = re.search(r'version=\'(\d\.\d\.\d)\'', setup_content).group(1)

if changes_version != setup_version:
    print('Version numbers differ')
    print('CHANGES.txt states: v' + changes_version)
    print('setup.py states:    v' + setup_version)
    exit(1)