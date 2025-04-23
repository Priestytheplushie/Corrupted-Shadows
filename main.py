# Corrupted Shadows

# Imports
import time
import random
import cmd
import sys
import textwrap
from player import Player
from title import title_screen
from new_game import character_creation
from enemies import *
from battle import *
from item_factory import create_item
from chapter1 import *

player = title_screen()

if player:
    chapter_1(player)
else:
    print(Fore.RED+"Character creation failed. Please try again.")