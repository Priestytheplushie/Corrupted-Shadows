from colorama import Fore, Style
import random
import math

def heal_player_value(player, healing_amount):
    healed_hp = min(player.hp + healing_amount, player.max_hp)
    player.hp = healed_hp
    print(Fore.GREEN + "You heal for " + str(healing_amount) + " HP, bringing your health to " + str(player.hp) + "/" + str(player.max_hp) + ".")

def heal_player_precent(player, healing_percentage):
    # Calculate the healing amount based on the percentage of max HP
    healing_amount = int(player.max_hp * (healing_percentage / 100))
    
    # Ensure the healing does not exceed the amount needed to reach max HP
    healing_amount = min(healing_amount, player.max_hp - player.hp)
    
    # Apply the healing
    player.hp += healing_amount
    
    # Print the result
    print(Fore.GREEN + "You heal for " + str(healing_amount) + " HP, bringing your health to " + str(player.hp) + "/" + str(player.max_hp) + ".")