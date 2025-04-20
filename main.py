# Priesty's Quest

import time
import random
import cmd
import sys
import textwrap
from colorama import Fore, Back, Style

# Player Setup #

class Player:
    def __init__(self):
        self.name = ""
        self.hp = 0
        self.strength = 0
        self.speed = 0
        self.intelligence = 0
        self.defense = 0
        self.money = 0
        self.status_effects = []
player = Player()