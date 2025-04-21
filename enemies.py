from colorama import Fore, Style
import random
import math
from attack import calculate_attack

# Generic Enemy Class
class Enemy:
    def __init__(self,name,level,hp,strength,speed,intelligence,defense,weapon=None):
        self.name = name
        self.hp = hp
        self.strength = strength
        self.speed = speed
        self.intelligence = intelligence
        self.defense = defense
        self.max_hp = self.hp
        self.status_effects = []
        self.weapon = weapon 
        self.level = level

    def basic_attack(self, player):
        damage = calculate_attack(self.strength, 0)
        player.hp -= damage
        print(self.name + " attacks " + player.name + " for " + str(damage) + " damage!")
        print("")
        print(player.name + " remaining HP: " + str(player.hp))
        print("")

    def choose_action(self, target):
        self.basic_attack(target)

    # Generic Attack


# Goblin Class
class Goblin(Enemy):
    def __init__(self, level):
        self.name = Fore.RED + "Goblin" + Fore.WHITE
        self.hp = 30 + level
        self.strength = 5 + level
        self.speed = 10
        self.intelligence = 0
        self.defense = level
        self.max_hp = self.hp
        self.weapon = None
        self.level = level
    
    def rob(self, player):
        if player.money > 0:
            stolen_money = random.randint(1, player.money)
            player.money -= stolen_money
            damage = random.randint(self.strength - 2, self.strength + 2)  # Robbing also deals damage
            player.hp -= damage
            print(self.name + " attempts to rob " + player.name + ", stealing $" + str(stolen_money) + " and dealing " + str(damage) + " damage!")
            print("")
            print(player.name + "'s remaining money: $" + str(player.money))
            print("")
            print(player.name + " remaining HP: " + str(player.hp))
            print('')
        else:
            print(self.name + " tried to rob " + player.name + ", but they have no money to steal.")
            print("")

    def choose_action(self, target):
        if target.money > 0 and random.random() < 0.3:
            self.rob(target)
        else:
            self.basic_attack(target)