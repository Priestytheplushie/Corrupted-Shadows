from colorama import Fore, Style
import random
import time
from inventory import Inventory
from items import *
from attack import calculate_attack
from item_data import *
from text_utils import *

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

        # Arena Specific Attributes
        self.battle_shifter = False
        self.reroll_used = 0
        self.corruption = 0

    def punch(self, enemy):
        # Punch uses base strength and weapon damage isn't factored in
        if random.random() < 0.15:  # Miss chance
            print(Fore.YELLOW + self.name + " swings at " + enemy.name + " but misses!" + Fore.WHITE)
            print("")
            time.sleep(1)
            return
        # Calculate damage with a small variation
        raw_damage = calculate_attack(self.strength)
        damage = max(1, raw_damage - enemy.defense)
    
        enemy.hp -= damage
        print(self.name + " punches " + enemy.name + " for " + str(damage) + " damage!")
        if enemy.defense > 0:
            print(Fore.LIGHTBLACK_EX + "(Reduced from " + str(raw_damage) + " by defense)" + Fore.WHITE)
        print("")
        print(enemy.name + " remaining HP: " + str(enemy.hp))
        print("")

    def attack(self, enemy):
        # Check for miss chance
        if random.random() < 0.15:
            print(Fore.YELLOW + self.name + " swings at " + enemy.name + " but misses!" + Fore.WHITE)
            print("")
            time.sleep(1)
            return
        raw_damage = calculate_attack(self.strength, self.weapon.damage if self.weapon else 0)
        damage = max(1, raw_damage - enemy.defense)
        enemy.hp -= damage
        print(self.name + " attacks " + enemy.name + " with " + (self.weapon.name if self.weapon else 'bare hands') + " for " + str(damage) + " damage!")
        if enemy.defense > 0:
            print(Fore.LIGHTBLACK_EX + "(Reduced from " + str(raw_damage) + " by defense)" + Fore.WHITE)
            print("")
        print("")
        print(enemy.name + " remaining HP: " + str(enemy.hp))
        print("")
        time.sleep(1)

    
    def show_inventory(self):
        self.inventory.show_inventory()
    
    def use_item(self, index, target=None):
        self.inventory.use_item(self, index, target)

    def equip_weapon(self, weapon,silent=False):
        self.weapon = weapon
        if not silent:
            print(self.weapon, "equipped.")

    def unequip_weapon(self):
        self.weapon = None  
        print("Weapon unequipped.")

    def check_level_up(player):
        level_thresholds = {
            2: 100,
            3: 300,
            4: 600,
            5: 1000,
            6: 1500,
            7: 2100,
            8: 2800,
            9: 3700,
            10: 4800,
            # Add more thresholds as needed
        }

        while player.level + 1 in level_thresholds and player.xp >= level_thresholds[player.level + 1]:
            old_level = player.level
            player.level += 1
            player.max_hp += 10
            player.hp = player.max_hp
            player.strength += 2
            player.defense += 1
            player.intelligence += 1

            # Notify the player of the level-up
            print("")
            animate_title(Fore.MAGENTA + "LEVEL UP!" + Style.RESET_ALL)
            animate_title(f"{player.name} Leveled Up! {old_level} ---> {player.level}")
            animate_title("HP: " + str(player.max_hp))
            animate_title("Strength: " + str(player.strength))
            animate_title("Defense: " + str(player.defense))
            animate_title("Intelligence: " + str(player.intelligence))
            print("")

            # Wait for the player to acknowledge the level-up
            input((center_text(Fore.YELLOW + "Press Enter to continue..." + Fore.RESET)))

        # Ensure the function exits cleanly
        return

    def apply_status(self, effect, duration):
        self.status_effects.append({'effect': effect, 'duration': duration})
        typewriter(self.name + " is affected by " + effect + " for " + str(duration) + " turn(s).")

    def remove_status(self, effect, duration):
        self.status_effects = [se for se in self.status_effects if se['effect'] != effect]
    
    def process_status_effects(self):
        updated_effects = []
        for effect in self.status_effects:
            effect['duration'] -= 1

            if effect['effect'] == 'stagger':
                self.speed = max(1, self.speed - 2)
                if effect['duration'] <= 0:
                    self.speed += 2
                else:
                    updated_effects.append(effect)

            elif effect['effect'] == 'defending':
                if effect['duration'] <= 0:
                    self.defense -= effect['boost']
                    typewriter(Fore.BLUE + self.name + "'s defense boost has faded." + Fore.RESET)
                else:
                    updated_effects.append(effect)

            else:
                if effect['duration'] > 0:
                    updated_effects.append(effect)

        self.status_effects = updated_effects

    def is_staggered(self):
        return any(se['effect'] == 'stagger' for se in self.status_effects)
    
    def defend(self):
        for effect in self.status_effects:
            if effect['effect'] == 'defending':
                effect['duration'] = random.randint(3, 5)
                typewriter(Fore.CYAN + self.name + " refreshes their defensive stance!" + Fore.RESET)
                print("")
                return

        duration = random.randint(3, 5)
        percent_increase = max(1, int(self.defense * 0.1))
        level_bonus = self.level
        defense_boost = percent_increase + level_bonus

        self.defense += defense_boost
        self.status_effects.append({'effect': 'defending', 'duration': duration, 'boost': defense_boost})

        typewriter(Fore.BLUE + self.name + " braces for impact, raising defense by " +
                str(defense_boost) + " for " + str(duration) + " turns!" + Fore.RESET)
        print("")