from colorama import Fore, Style
import random
import math
import time
from text_utils import *
from enemies import *

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
        self.max_durability = durability
        self.name = name
    def attack(self,user,target):
        if self.durability <= 0:
            print(self.name + " is broken and can't be used!")
            print("")
            user.weapon = None
            del self
            return
        else:
            if random.random() < 0.10:
                print(Fore.YELLOW + user.name + " swings at " + target.name + " but misses!" + Fore.WHITE)
                print("")
                time.sleep(1)
                return
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
        self.name = name
        self.healing_amount = healing_amount
        self.quantity = quantity
    def use(self, player):
        if self.quantity <= 0:
            print(Fore.RED + self.name + " is out of stock!" + Style.RESET_ALL)
            return
        player.hp += self.healing_amount
        self.quantity -= 1
        print(Fore.GREEN + player.name + " uses " + self.name + " and heals " + str(self.healing_amount) + " HP!" + Style.RESET_ALL)


class UseableItem(Item): # Generic Useable Item Class to Import From
    def __init__(self, name, description, uses):
        super().__init__(name, description)
        self.durability = uses
        self.max_durability = uses

    def use(self, player, targets):
        if self.durability <= 0:
            print(Fore.RED + self.name + " is out of uses!" + Style.RESET_ALL)
            del self
            return
        if not isinstance(targets, list):
            targets = [targets]

        for target in targets:
            if isinstance(target, Enemy):
                self.durability -= 1
                print(Fore.RED+self.name+" had no effect!")
                print("")
            else:
                print(Fore.RED + self.name + " Flute had no effect on " + target.name + Style.RESET_ALL)
                print("")
                return

class CleansingFlute(UseableItem):
    def __init__(self, name, description, uses):
        super().__init__(name, description, uses)
        self.durability = uses
        self.max_durability = uses

    def use(self, player, targets):
        if self.durability <= 0:
            print(Fore.RED + self.name + " is out of uses!" + Style.RESET_ALL)
            del self
            return
        
        if not isinstance(targets, list):
            targets = [targets]

        for target in targets:
            if isinstance(target, Enemy) and target.corrupted:
                self.durability -= 1
                print(Fore.GREEN + "The Cleansing Flute has cleansed " + target.name + "!" + Style.RESET_ALL)
                print("")
                target.cleanse()
            else:
                print(Fore.RED + "The Cleansing Flute had no effect on " + target.name + Style.RESET_ALL)
                print("")
                return
        
