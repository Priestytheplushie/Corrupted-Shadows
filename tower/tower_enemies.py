from colorama import Fore, Style
import random
import time
from game_data import *
from attack import calculate_attack

class Enemy:
    def __init__(self, name, level, hp=None, strength=None, defense=None, speed=None, intelligence=None, weapon=None, loot_table_key="none"):
        self.name = name
        self.real_name = name
        self.weapon = weapon
        self.loot_table_key = loot_table_key
        self.level = level
        self.status_effects = []
        self.hp = hp
        self.strength = strength
        self.defense = defense
        self.speed = speed
        self.intelligence = intelligence
        self.base_hp = 10  # Default value, used if hp is not provided
        self.base_strength = 2  # Default value, used if strength is not provided
        self.base_defense = 1  # Default value, used if defense is not provided
        self.base_speed = 5  # Default value, used if speed is not provided
        self.base_intelligence = 3  # Default value, used if intelligence is not provided
        self.corrupted = False  # Default to False, can be set for corrupted enemies

        # If stats are not provided, use the base ones
        if self.hp is None:
            self.hp = max(self.base_hp * self.level, self.base_hp * 10)  # Ensure HP isn't too low
        if self.strength is None:
            self.strength = self.base_strength * self.level
        if self.defense is None:
            self.defense = self.base_defense * self.level
        if self.speed is None:
            self.speed = self.base_speed + self.level
        if self.intelligence is None:
            self.intelligence = self.base_intelligence + self.level

        self.max_hp = self.hp  # Set max HP based on current HP

        self.adjust_for_difficulty()
        self.calculate_stats()

    def adjust_for_difficulty(self):
        global difficulty

        # Difficulty multipliers for level scaling
        difficulty_multipliers = {
            "easy": 0.75,
            "normal": 1.0,
            "hard": 1.5,
            "hardcore": 2.0
        }

        # Apply the difficulty multiplier to the enemy's level
        level_multiplier = difficulty_multipliers.get(difficulty, 1.0)

        # Calculate the new level
        adjusted_level = int(self.level * level_multiplier)

        # Ensure the level doesn't go below 1
        adjusted_level = max(1, adjusted_level)

        self.level = adjusted_level

        # Apply the difficulty multiplier to the enemy's base stats
        multiplier = difficulty_multipliers.get(difficulty, 1.0)

        # Ensure HP is calculated as base HP + difficulty-adjusted value
        self.hp = self.base_hp + int(self.base_hp * (multiplier - 1))
        self.max_hp = self.hp
        
    def calculate_stats(self):
        # Scale stats based on level
        self.hp = self.base_hp * self.level
        self.strength = self.base_strength * self.level
        self.defense = self.base_defense * self.level
        self.speed = self.base_speed + self.level  # Speed grows linearly
        self.intelligence = self.base_intelligence + self.level  # Intelligence grows linearly

        # Set max HP based on recalculated HP
        self.max_hp = self.hp

    def apply_status(self, effect_name, duration):
        found = False
        for effect in self.status_effects:
            if effect['name'] == effect_name:
                effect['duration'] = duration
                found = True
        if not found:
            self.status_effects.append({'name': effect_name, 'duration': duration})

    def has_status(self, effect_name):
        for effect in self.status_effects:
            if effect['name'] == effect_name:
                return True
        return False

    def tick_status_effects(self):
        remaining = []
        for effect in self.status_effects:
            effect['duration'] -= 1
            if effect['duration'] > 0:
                remaining.append(effect)
            else:
                print(self.name + " is no longer affected by " + effect['name'] + ".")
                print("")
        self.status_effects = remaining

    def basic_attack(self, player):
        if random.random() < 0.10:
            print(Fore.YELLOW + self.name + " swings at " + player.name + " but misses!" + Fore.WHITE)
            print("")
            time.sleep(1)
            return
        raw_damage = calculate_attack(self.strength, 0)
        damage = max(1, raw_damage - player.defense)
        player.hp -= damage
        print(self.name + " attacks " + player.name + " for " + str(damage) + " damage!")
        print("")
        if player.defense > 0:
            print(Fore.LIGHTBLACK_EX + "(Reduced from " + str(raw_damage) + " by defense)" + Fore.WHITE)
            print("")

        print(player.name + " remaining HP: " + str(player.hp))
        print("")

    def choose_action(self, target):
        if self.has_status('stagger'):
            print(self.name + " is staggered and misses their turn!")
            print("")
            return
        self.basic_attack(target)

    def reveal_identity(self):
        self.name = self.real_name
        print("")
        print(Fore.YELLOW + "The veil lifts... it's a " + self.real_name + "!" + Fore.WHITE)
        print("")

        if self.corrupted:
            print(Fore.RED + "\nA dark aura surrounds it... This enemy is CORRUPTED!")
            print(Fore.MAGENTA + "The corruption has twisted its form and powers, making it far more dangerous than before!" + Fore.WHITE)
        else:
            print(Fore.GREEN + "This enemy appears to be normal, free of corruption." + Fore.WHITE)


class CorruptedHuman(Enemy):
    def __init__(self, level, weapon=None, loot_table_key="none"):
        self.base_hp = 50
        self.base_strength = 10
        self.base_defense = 5
        self.base_speed = 5
        self.base_intelligence = 100
        self.real_name = Fore.GREEN+"Corrupted Human"+Fore.WHITE

        super().__init__(name=Fore.MAGENTA+"???"+Fore.WHITE, level=level, weapon=weapon, loot_table_key=loot_table_key)
        self.corrupted = True
        self.max_hp = self.hp

    def use_item(self):
        items = [
            "Health Potion",
            "Strength Potion",
            "Defense Potion"
        ]

        used_item = random.choice(items)

        if used_item == "Health Potion":
            heal_amount = 25
            print(self.name, Fore.WHITE + "used Health Potion and restored", Fore.RED + str(heal_amount), Fore.WHITE + "HP!")
            time.sleep(1)

            # Prevent over-healing
            self.hp = min(self.hp + heal_amount, self.max_hp)  # Ensure HP doesn't exceed max HP

        elif used_item == "Strength Potion":
            print(self.name, Fore.WHITE + "used Strength Potion and increased strength by", Fore.RED + "5", Fore.WHITE)
            time.sleep(1)
            self.strength += 5

        elif used_item == "Defense Potion":
            print(self.name, Fore.WHITE + "used Defense Potion and increased Defense by", Fore.RED + "5", Fore.WHITE)
            time.sleep(1)
            self.defense += 5

    def choose_action(self, target):
        if self.has_status('stagger'):
            print(self.name + " is staggered and misses their turn!")
            print("")
            return
        if random.random() < 0.3:
            self.use_item()
        else:
            self.basic_attack(target)


class CorruptedWarrior(Enemy):
    def __init__(self, level, weapon=None, loot_table_key="none"):
        self.base_hp = 45
        self.base_strength = 20
        self.base_defense = 10
        self.base_speed = 0
        self.base_intelligence = 50
        self.real_name = Fore.GREEN+"Corrupted Warrior"+Fore.WHITE

        super().__init__(name=Fore.MAGENTA+"Warrior"+Fore.WHITE, level=level, weapon=weapon, loot_table_key=loot_table_key)
        self.corrupted = True
        self.max_hp = self.hp

    def battle_cry(self):
        print(Fore.WHITE+self.name+Fore.WHITE+" roars into the air, increasing their natural strength by +1")
        self.strength += 1

    def heavy_charge(self, player):
        if random.random() < 0.30:
            print(Fore.YELLOW + self.name +Fore.YELLOW+ " charges at " + player.name + " but misses!" + Fore.WHITE)
            print("")
            time.sleep(1)
            return
        raw_damage = calculate_attack(self.strength, 10)
        damage = max(1, raw_damage - player.defense)
        player.hp -= damage
        print(self.name + " charges at " + player.name + " dealing " + str(damage) + " damage!")
        print("")
        if player.defense > 0:
            print(Fore.LIGHTBLACK_EX + "(Reduced from " + str(raw_damage) + " by defense)" + Fore.WHITE)
            print("")

        print(player.name + " remaining HP: " + str(player.hp))
        print("")
        if random.random() < 0.2:
            time.sleep(1)
            player.apply_status('stagger', 1)

    def choose_action(self, target):
        if self.has_status('stagger'):
            print(self.name + " is staggered and misses their turn!")
            print("")
            return
        if random.random() < 0.3:
            self.battle_cry()
        else:
            if random.randint(0, 100) < 40:
                self.heavy_charge(target)
            else:
                self.basic_attack(target)

class CorruptedMage(Enemy):
    def __init__(self, level, weapon=None, loot_table_key="none"):
        self.base_hp = 25
        self.base_strength = 5
        self.base_defense = 2
        self.base_speed = 4
        self.base_intelligence = 20
        self.real_name = Fore.GREEN+"Corrupted Mage"+Fore.WHITE

        super().__init__(name=Fore.MAGENTA+"Mage"+Fore.WHITE, level=level, weapon=weapon, loot_table_key=loot_table_key)
        self.corrupted = True
        self.max_hp = self.hp

    def fireball(self, target):
        if random.random() < 0.2:
            print(Fore.YELLOW + self.name + " casts Fireball, but it misses!" + Fore.WHITE)
            print("")
            time.sleep(1)
            return
        damage = random.randint(10, 20)  # Fireball damage
        print(self.name + " casts Fireball at " + target.name + " for " + str(damage) + " damage!")
        target.hp -= damage
        print(target.name + " remaining HP: " + str(target.hp))
        print("")
        
        # 30% chance to burn an item (rendering it unusable)
        if random.random() < 0.30:
            burned_item = random.choice(target.inventory.items)
            print(Fore.RED + burned_item.name + " was burned and is now unusable!" + Fore.WHITE)
            target.inventory.remove_item(burned_item)

    def energy_ball(self, target):
        damage = random.randint(5, 15)  # Energy Ball damage
        print(self.name + " casts Energy Ball at " + target.name + " for " + str(damage) + " damage!")
        target.hp -= damage
        print(target.name + " remaining HP: " + str(target.hp))
        print("")

    def choose_action(self, target):
        if self.has_status('stagger'):
            print(self.name + " is staggered and misses their turn!")
            print("")
            return
        # 60% chance for Fireball, 40% for Energy Ball
        if random.random() < 0.6:
            self.fireball(target)
        else:
            self.energy_ball(target)
