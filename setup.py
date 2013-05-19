from setuptools import setup

setup(
    name='Vengeance',
    version='1.0.0',
    author='Matthew Murdoch',
    author_email='matthew.murdoch.0@gmail.com',
    packages=['vengeance', 'vengeance.test'],
    scripts=['bin/example_game.py'],
    url='http://pypi.python.org/pypi/Vengeance/',
    license='LICENSE.txt',
    description='Text-based adventure game engine',
    long_description=open('README.txt').read(),
)