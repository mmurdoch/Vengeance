from setuptools import setup

setup(
    name='Vengeance',
    version='1.1.1',
    author='Matthew Murdoch',
    author_email='matthew.murdoch.0@gmail.com',
    packages=['vengeance', 'vengeance.test'],
    scripts=['bin/declaratively_defined_game.py', 'bin/procedurally_defined_game.py', 'bin/embed_engine.py', 'bin/game_testing.py'],
    url='http://pypi.python.org/pypi/Vengeance/',
    license='LICENSE.txt',
    description='Text-based adventure game engine',
    long_description=open('README.txt').read(),
)