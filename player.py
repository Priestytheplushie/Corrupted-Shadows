from colorama import Fore, Style
import random
import math
from inventory import Inventory
from items import *
from attack import calculate_attack
from text_utils import *

# Generic Player Class

class Player:
    def __init__(self, name, hp, strength, speed, intelligence, defense, money, weapon=None):
        self.name = name
        self.hp = hp
        self.strength = strength
        self.speed = speed
        self.intelligence = intelligence
        self.defense = defense
        self.money = money
        self.max_hp = self.hp
        self.weapon = weapon
        self.xp = 0
        self.level = 1
        self.status_effects = []
        self.inventory = Inventory() 

    def punch(self, enemy):
        damage = calculate_attack(self.strength, 0)  # No weapon bonus for punch
        enemy.hp -= damage
        print(self.name + " punches " + enemy.name + " for " + str(damage) + " damage!")
        print("")
        print(enemy.name + " remaining HP: " + str(enemy.hp))
        print("")

    def attack(self, enemy):
        damage = calculate_attack(self.strength, self.weapon.damage if self.weapon else 0)
        enemy.hp -= damage
        print(self.name + " attacks " + enemy.name + " with " + (self.weapon.name if self.weapon else 'bare hands') + " for " + str(damage) + " damage!")
        print("")
        print(enemy.name + " remaining HP: " + str(enemy.hp))
        print("")
        time.sleep(1)
    
    def show_inventory(self):
        self.inventory.show_inventory()
    
    def use_item(self, index, target=None):
        self.inventory.use_item(self, index, target)

    def level_up(self):
        level_thresholds = {
            2: 100,
            3: 250,
            4: 450,
            5: 700,
            6: 1000,
            7: 1350,
            8: 1750,
            9: 2200,
            10: 2700
        }

        while self.level + 1 in level_thresholds and self.xp >= level_thresholds[self.level + 1]:
            self.level += 1
            self.max_hp += 10
            self.hp = self.max_hp
            self.strength += 2
            self.defense += 1
            self.intelligence += 1

            typewriter("")
            typewriter(center_text(Fore.MAGENTA + "LEVEL UP!" + Style.RESET_ALL))
            typewriter(center_text("You are now level " + str(self.level) + "!"))
            typewriter(center_text("HP: " + str(self.max_hp)))
            typewriter(center_text("Strength: " + str(self.strength)))
            typewriter(center_text("Defense: " + str(self.defense)))
            typewriter(center_text("Intelligence: " + str(self.intelligence)))
            typewriter("")

            input(center_text("Press Enter to continue..."))