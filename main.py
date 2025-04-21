# Priesty's Quest

import time
import random
import cmd
import sys
import textwrap
from player import Player
from title_screen import title_screen
from new_game import character_creation, roll_intellignece

title_screen()

player_name = character_creation
intellignece = roll_intellignece

player = Player(player_name,100,5,5,intellignece,0,1000)

