from colorama import Fore, Style
import random
import math
import time

class Item:
    def __init__(self,name,description):
        self.name = name
        self.description = description
    def __str__(self):
        return self.name
    def use(self,target):
        print(Fore.RED+self.name,"has no effect!")
        print("")

class Weapon(Item):
    def __init__(self, name, description, damage, durability):
        super().__init__(name, description)
        self.damage = damage
        self.durability = durability
    def attack(self,user,target):
        if self.durability <= 0:
            print(self.name + " is broken and can't be used!")
            print("")
            user.weapon = None
            return
        else:
            target.hp -= self.damage
            self.durability -= 1
            print(user.name + " attacks with " + self.name + ", dealing " + str(self.damage) + " damage to " + target.name + "!")
            print("")
            time.sleep(1)
            print(self.name + " durability: " + str(self.durability))
            print("")
    
    def equip(self, player):
        player.weapon = self
        print(Fore.CYAN + player.name + " equipped " + self.name + "!" + Style.RESET_ALL)
        print("")

class Potion(Item):
    def __init__(self, name, description, healing_amount, quantity):
        super().__init__(name, description)
        self.healing_amount = healing_amount
        self.quantity = quantity
    def use(self, player):
        if self.quantity <= 0:
            print(Fore.RED + self.name + " is out of stock!" + Style.RESET_ALL)
            return
        player.hp += self.healing_amount
        self.quantity -= 1
        print(Fore.GREEN + player.name + " uses " + self.name + " and heals " + str(self.healing_amount) + " HP!" + Style.RESET_ALL)