from colorama import Fore, Style
import random
import math

def heal_player(player, healing_amount):
    healed_hp = min(player.hp + healing_amount, player.max_hp)
    player.hp = healed_hp
    print(Fore.GREEN + "You heal for " + str(healing_amount) + " HP, bringing your health to " + str(player.hp) + "/" + str(player.max_hp) + ".")

def heal_player(player, healing_percentage):
    healing_amount = int(player.max_hp * (healing_percentage / 100))
    healed_hp = min(player.hp + healing_amount, player.max_hp)
    player.hp = healed_hp
    print(Fore.GREEN + "You heal for " + str(healing_amount) + " HP, bringing your health to " + str(player.hp) + "/" + str(player.max_hp) + ".")