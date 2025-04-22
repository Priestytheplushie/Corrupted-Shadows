# Priesty's Quest

# Imports
import time
import random
import cmd
import sys
import textwrap
from player import Player
from title_screen import title_screen
from new_game import character_creation, roll_intellignece
from enemies import *
from battle import *

title_screen() # Display game title

# Set stats based on new_game.py
player_name = character_creation()
intellignece = roll_intellignece()

player = Player(player_name,100,10,5,intellignece,0,1000) # Create Player Class
goblin = Goblin(5)

battle(player,goblin) # Test Battle