from distutils.core import setup

setup(
    name='Adventure',
    version='0.1.0',
    author='Matthew Murdoch',
    author_email='matthew.murdoch.0@gmail.com',
    packages=['adventure', 'adventure.test'],
    scripts=['bin/example_game.py'],
    url='http://pypi.python.org/pypi/Adventure/',
    license='LICENSE.txt',
    description='Text-based adventure game engine',
    long_description=open('README.txt').read(),
    install_requires=[
    ],
)