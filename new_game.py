from player import Player
from colorama import Fore, Style
import random
import sys
import time
import os


def roll_intellignece():
    intellignece = random.randint(0,200)
    return intellignece

def character_creation():
    os.system('cls' if os.name == 'nt' else 'clear') 
    name = input(Fore.YELLOW+"What is your name? > ")
    while name == '':
        print(Fore.RED+"You must enter a name!")
        print("")
        name = input(Fore.YELLOW+"What is your name? > ")
    roll_intellignece()
    return name