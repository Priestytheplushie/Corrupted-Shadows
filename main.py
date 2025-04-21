# Priesty's Quest

import time
import random
import cmd
import sys
import textwrap
from player import Player
from title_screen import title_screen
from new_game import character_creation, roll_intellignece
from enemies import *

title_screen()

player_name = character_creation
intellignece = roll_intellignece

player = Player(player_name,100,5,5,intellignece,0,1000)

test = Goblin(5)


# Test Combat Loop --- NOT FOR ACTAUL GAME
while player.hp > 0:
    test.rob(player)
    time.sleep(2)
    print(Fore.WHITE+str(player_name),"has",player.hp,"health left!")
    print("")