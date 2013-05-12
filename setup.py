from setuptools import setup

setup(
    name='Vengence',
    version='0.1.0',
    author='Matthew Murdoch',
    author_email='matthew.murdoch.0@gmail.com',
    packages=['vengence', 'vengence.test'],
    scripts=['bin/example_game.py'],
    url='http://pypi.python.org/pypi/Vengence/',
    license='LICENSE.txt',
    description='Text-based adventure game engine',
    long_description=open('README.txt').read(),
)