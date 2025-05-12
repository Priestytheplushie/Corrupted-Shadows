# Corrupted Shadows

# Imports
import time
import random
import cmd
import sys
import textwrap
import colorama
from player import Player
from title import title_screen
from game_data import tower
from enemies import *
from battle import *
from chapter1 import *
from tower.tower_main import main
from tower.tower_screens import corrupted_death_screen
from discord import connect_to_discord, update_presence, disconnect_from_discord

try:
    connect_to_discord()
except Exception as e:
    print("Discord connection failed:", e)


while True:
    player, mode = title_screen()

    if player and mode == "tower":
        main(player)
    elif player and mode == "gauntlet":
        continue
    elif player:
        chapter_1(player)
    else:
        print(Fore.RED+"Character creation failed. Please try again.")