from colorama import Fore, Style
import random
import time
from text_utils import *
from enemies import *

class Item:
    def __init__(self, name, description, base_value):
        self.name = name
        self.description = description
        self.base_value = base_value
        self.value = base_value 

    def __str__(self):
        return self.name

    def use(self, target):
        print(Fore.RED + self.name + " has no effect!")
        print("")

    def update_value(self):
        raise NotImplementedError("This method should be overridden by subclasses.")

class Weapon(Item):
    def __init__(self, name, description, damage, durability, base_value):
        super().__init__(name, description, base_value)
        self.damage = damage
        self.durability = durability
        self.max_durability = durability

    def attack(self, user, target):
        total_damage = self.damage + user.strength
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
            target.hp -= total_damage
            self.durability -= 1
            self.update_value()  # Update the value after each attack
            print(user.name + " attacks with " + self.name + ", dealing " + str(total_damage) + " damage to " + target.name + "!")
            print(target.name + " remaining HP: " + str(target.hp))
            print(self.name + " durability: " + str(self.durability))
            print("")

    def equip(self, player):
        player.weapon = self
        print(Fore.CYAN + player.name + " equipped " + self.name + "!" + Style.RESET_ALL)
        print("")

    def update_value(self):
        """Update the value based on durability."""
        self.value = max(self.base_value * (self.durability / self.max_durability), 0)
        print(self.name + " value is now " + str(self.value) + " due to reduced durability.")

class OrcsMace(Weapon):
    def __init__(self, name, description, damage, durability, base_value):
        super().__init__(name, description, damage, durability, base_value)

    def attack(self, user, target):
        total_damage = self.damage + user.strength
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
            target.hp -= total_damage
            self.durability -= 1
            self.update_value()  # Update value based on durability loss
            print(user.name + " smashes " + target.name + " with " + self.name + ", dealing " + str(total_damage) + " damage!")
            print(target.name + " remaining HP: " + str(target.hp))
            print(self.name + " durability: " + str(self.durability))
            if random.random() < 0.3:
                target.apply_status('stagger', 2)
            print("")

class Potion(Item):
    def __init__(self, name, description, healing_amount, quantity, base_value):
        super().__init__(name, description, base_value)
        self.healing_amount = healing_amount
        self.quantity = quantity

    def use(self, player):
        if self.quantity <= 0:
            print(Fore.RED + self.name + " is out of stock!" + Style.RESET_ALL)
            return
        player.hp += self.healing_amount
        self.quantity -= 1
        self.update_value()  # Update value after use
        print(Fore.GREEN + player.name + " uses " + self.name + " and heals " + str(self.healing_amount) + " HP!" + Style.RESET_ALL)

    def update_value(self):
        """Update the value based on remaining quantity."""
        self.value = max(self.base_value * (self.quantity / 5), 0)  # Example: Value decreases as quantity goes down
        print(self.name + " value is now " + str(self.value) + " due to reduced quantity.")

class UseableItem(Item):
    def __init__(self, name, description, uses, base_value):
        super().__init__(name, description, base_value)
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
                self.update_value()  # Update value after use
                print(Fore.RED + self.name + " had no effect!")
                print("")
            else:
                print(Fore.RED + self.name + " had no effect on " + target.name + Style.RESET_ALL)
                print("")
                return

    def update_value(self):
        """Update the value based on remaining uses."""
        self.value = max(self.base_value * (self.durability / self.max_durability), 0)
        print(self.name + " value is now " + str(self.value) + " due to remaining uses.")

class CleansingFlute(UseableItem):
    def __init__(self, name, description, uses, base_value):
        super().__init__(name, description, uses, base_value)

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
                self.update_value()  # Update value after use
                print(Fore.GREEN + "The Cleansing Flute has cleansed " + target.name + "!" + Style.RESET_ALL)
                print("")
                target.cleanse()
            else:
                print(Fore.RED + "The Cleansing Flute had no effect on " + target.name + Style.RESET_ALL)
                print("")

