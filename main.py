# Corrupted Shadows

# Imports
import time
import random
import cmd
import sys
import textwrap
from player import Player
from title import title_screen
from enemies import *
from battle import *
from chapter1 import *

player = title_screen()

if player:
    chapter_1(player)
else:
    print(Fore.RED+"Character creation failed. Please try again.")