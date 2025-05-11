import random
from colorama import Fore
from game_data import *

def calculate_attack(base_strength, weapon_damage=0, crit_chance=0.1, crit_multiplier=2.0,
                     attack_buff=1.0, weapon_scaling=0.2, element_damage=0,
                     min_damage=10, max_damage=50):
    
    strength_variation = random.randint(-2, 2)
    weapon_scaling_damage = int(base_strength * weapon_scaling)  # Convert to int

    base_damage = base_strength + strength_variation + weapon_damage + weapon_scaling_damage
    total_damage = int(base_damage * attack_buff + element_damage)  # Round down to int

    # Clamp to range
    if total_damage < min_damage:
        total_damage = random.randint(min_damage, max_damage)
    elif total_damage > max_damage:
        total_damage = max_damage

    # Critical hit check
    if random.random() < crit_chance:
        total_damage = int(total_damage * crit_multiplier)  # Round down
        print(Fore.RED + "Critical Hit!" + Fore.WHITE)

    return total_damage


