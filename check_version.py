import datetime
import re
import sys

changes_file = open('CHANGES.txt', 'r')
changes_first_line = changes_file.readline()
changes_match = re.match(r'v(\d\.\d\.\d), (.*)',
                           changes_first_line)
changes_version = changes_match.group(1)
changes_release_date = changes_match.group(2)

today = str(datetime.date.today())

setup_file = open('setup.py', 'r')
setup_content = setup_file.read()
setup_version = re.search(r'version=\'(\d\.\d\.\d)\'',
                          setup_content).group(1)

sphinx_file = open('sphinx/conf.py', 'r')
sphinx_content = sphinx_file.read()
sphinx_version = re.search(r'version = \'(\d\.\d)\'',
                           sphinx_content).group(1)
sphinx_release = re.search(r'release = \'(\d\.\d\.\d)\'',
                           sphinx_content).group(1)

if changes_version != setup_version or changes_version != sphinx_release:
    print('Version numbers differ:')
    print('CHANGES.txt states:    v' + changes_version)
    print('setup.py states:       v' + setup_version)
    print('sphinx/conf.py states: v' + sphinx_release)
    exit(1)

if changes_release_date != today:
    print('Release date is not today:')
    print('CHANGES.txt states: ' + changes_release_date)
    print('Today is:           ' + today)
    exit(1)

if not sphinx_release.startswith(sphinx_version):
    print('Sphinx version configuration differs:')
    print('Sphinx version: ' + sphinx_version)
    print('Sphinx release: ' + sphinx_release)
    exit(1)