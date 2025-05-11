import random
from colorama import Fore
from game_data import *

def calculate_attack(base_strength, weapon_damage=0, crit_chance=0.1, crit_multiplier=2.0, attack_buff=1.0, weapon_scaling=0.2, element_damage=0, min_damage=10, max_damage=50):
    strength_variation = random.randint(-2, 2)
    weapon_scaling_damage = base_strength * weapon_scaling  # Weapon scaling effect
    total_damage = (base_strength + strength_variation + weapon_damage + weapon_scaling_damage) * attack_buff + element_damage
    
    # Ensure total damage is within the defined range
    total_damage = random.randint(min_damage, max_damage) if total_damage < min_damage else total_damage
    total_damage = total_damage if total_damage <= max_damage else max_damage
    
    # Check if critical hit occurs
    if random.random() < crit_chance:
        total_damage *= crit_multiplier  # Apply crit multiplier
        print(Fore.RED+"Critical Hit!")
        
    return total_damage

