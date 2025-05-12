from colorama import Fore, Style
import random
import math
import time
from text_utils import *
from enemies import *
from tower.tower_data import bonus_ap

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
class Weapon(Item):
    def __init__(self, name, description, damage, durability):
        super().__init__(name, description)
        self.damage = damage
        self.durability = durability
        self.max_durability = durability

    def attack(self, user, target):
        if self.durability <= 0:
            print(self.name + " is broken and can't be used!")
            print("")
            user.weapon = None
            del self
            return

        if random.random() < 0.10:  # 10% chance to miss
            print(Fore.YELLOW + user.name + " swings at " + target.name + " but misses!" + Fore.WHITE)
            print("")
            time.sleep(1)
            return

        # Use the global calculate_attack method
        total_damage = calculate_attack(
            base_strength=user.strength,
            weapon_damage=self.damage,
            crit_chance=0.1,  # 10% crit chance
            crit_multiplier=2.0,  # Critical hits deal double damage
            attack_buff=1.0,  # No additional buffs
            weapon_scaling=0.2,  # Weapon scaling factor
            element_damage=0,  # No elemental damage
            min_damage=5,  # Minimum damage
            max_damage=50  # Maximum damage
        )

        # Apply damage to the target
        target.hp -= total_damage
        self.durability -= 1

        # Display attack details
        print(user.name + " attacks with " + self.name + ", dealing " + str(total_damage) + " damage to " + target.name + "!")
        if target.defense < 0:
            print(Fore.LIGHTBLACK_EX + "(Reduced from " + str(total_damage) + " by defense)" + Fore.WHITE)
        print("")
        print(target.name + " remaining HP: " + str(target.hp))
        print("")
        time.sleep(1)
        print(self.name + " durability: " + str(self.durability))
        print("")
    
    def equip(self, player):
        player.weapon = self
        print(Fore.CYAN + player.name + " equipped " + self.name + "!" + Style.RESET_ALL)
        print("")

class OrcsMace(Weapon):
    def __init__(self, name, description, damage, durability):
        super().__init__(name, description, damage, durability)
        self.aoe = True
        self.damage = damage
        self.durability = durability
        self.max_durability = durability
        self.name = name
        self.aoe = True

    def attack(self, user, target):
            if self.durability <= 0:
                print(self.name + " is broken and can't be used!")
                print("")
                user.weapon = None
                del self
                return

            if random.random() < 0.10:  # 10% chance to miss
                print(Fore.YELLOW + user.name + " swings at " + target.name + " but misses!" + Fore.WHITE)
                print("")
                time.sleep(1)
                return

            # Use the global calculate_attack method
            total_damage = calculate_attack(
                base_strength=user.strength,
                weapon_damage=self.damage,
                crit_chance=0.1,  # 10% crit chance
                crit_multiplier=2.0,  # Critical hits deal double damage
                attack_buff=1.0,  # No additional buffs
                weapon_scaling=0.2,  # Weapon scaling factor
                element_damage=0,  # No elemental damage
                min_damage=5,  # Minimum damage
                max_damage=100  # Maximum damage
            )

            # Apply damage to the target
            target.hp -= total_damage
            self.durability -= 1

            # Display attack details
            print(user.name + " smashes " + target.name + " with " + self.name + ", dealing " + str(total_damage) + " damage!")
            if target.defense < 0:
                print(Fore.LIGHTBLACK_EX + "(Reduced from " + str(total_damage) + " by defense)" + Fore.WHITE)
            print("")
            print(target.name + " remaining HP: " + str(target.hp))
            print("")
            time.sleep(1)
            print(self.name + " durability: " + str(self.durability))
            print("")

            # 30% chance to apply stagger
            if random.random() < 0.3:
                target.apply_status('stagger', 2)
    
    def equip(self, player):
        player.weapon = self
        print(Fore.CYAN + player.name + " equipped " + self.name + "!" + Style.RESET_ALL)
        print("")

class AOEWeapon(Weapon):
    def __init__(self, name, description, damage, durability):
        super().__init__(name, description, damage, durability)
        self.aoe = True
        self.damage = damage
        self.durability = durability
        self.max_durability = durability
        self.name = name
        self.aoe = True

    def attack(self, user, target):
            if self.durability <= 0:
                print(self.name + " is broken and can't be used!")
                print("")
                user.weapon = None
                del self
                return

            if random.random() < 0.10:  # 10% chance to miss
                print(Fore.YELLOW + user.name + " spins out of control at " + target.name + " and misses!" + Fore.WHITE)
                print("")
                time.sleep(1)
                return

            # Use the global calculate_attack method
            total_damage = calculate_attack(
                base_strength=user.strength,
                weapon_damage=self.damage,
                crit_chance=0.1,  # 10% crit chance
                crit_multiplier=2.0,  # Critical hits deal double damage
                attack_buff=1.0,  # No additional buffs
                weapon_scaling=0.2,  # Weapon scaling factor
                element_damage=0,  # No elemental damage
                min_damage=5,  # Minimum damage
                max_damage=100  # Maximum damage
            )

            # Apply damage to the target
            target.hp -= total_damage
            self.durability -= 1

            # Display attack details
            print(user.name + " attacks " + target.name + " with " + self.name + ", dealing " + str(total_damage) + " damage!")
            if target.defense < 0:
                print(Fore.LIGHTBLACK_EX + "(Reduced from " + str(total_damage) + " by defense)" + Fore.WHITE)
            print("")
            print(target.name + " remaining HP: " + str(target.hp))
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
        if player.hp > player.max_hp:
            player.hp = player.max_hp
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

    used = False

    # Cleanse enemies
    for target in targets:
        if isinstance(target, Enemy) and target.corrupted:
            print(Fore.GREEN + "The Cleansing Flute has cleansed " + target.name + "!" + Style.RESET_ALL)
            target.cleanse()
            used = True
        elif isinstance(target, Enemy):
            print(Fore.YELLOW + target.name + " is not corrupted. The flute has no effect." + Style.RESET_ALL)

    # Cleanse player if needed
    if player.corruption > 0:
        amount = 25
        player.corruption = max(player.corruption - amount, 0)
        print(Fore.CYAN + "The Cleansing Flute's melody calms your soul..." + Style.RESET_ALL)
        print("Corruption reduced by " + str(amount) + "%. Current Corruption: " + str(player.corruption) + "%")
        used = True

    # Only reduce durability if it did something
    if used:
        self.durability -= 1
        print(Fore.MAGENTA + self.name + " has " + str(self.durability) + " uses remaining." + Style.RESET_ALL)
    else:
        print(Fore.RED + "The Cleansing Flute had no effect." + Style.RESET_ALL)