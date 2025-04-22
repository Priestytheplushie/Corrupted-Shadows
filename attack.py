import random
from colorama import Fore
from game_data import *

def calculate_attack(base_strength, weapon_damage):
    strength_variation = random.randint(-2, 2) 
    total_damage = base_strength + strength_variation + (weapon_damage if weapon_damage else 0) 
    return total_damage