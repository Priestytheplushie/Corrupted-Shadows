from colorama import Fore, Style
import random
import math
from attack import calculate_attack
from game_data import *
import time
from game_data import difficulty 

class Enemy:
    def __init__(self, name, level, hp, strength, speed, intelligence, defense, weapon=None):
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
        self.adjust_for_difficulty()

    def adjust_for_difficulty(self):
        global difficulty
        if difficulty <= 25:
            self.apply_debuffs()
        elif difficulty <= 50:
            self.apply_regular_buffs_debuffs()
        elif difficulty <= 100:
            self.apply_damage_buffs()

    def apply_debuffs(self):
        self.hp = max(1, self.hp - random.randint(1, 5))
        self.strength = max(1, self.strength - random.randint(1, 3))
        self.defense = max(0, self.defense - random.randint(0, 2))

    def apply_regular_buffs_debuffs(self):
        if random.random() < 0.5:
            self.hp += random.randint(1, 5)
            self.strength += random.randint(1, 2)
        else:
            self.defense -= random.randint(0, 2)

    def apply_damage_buffs(self):
        self.strength += random.randint(3, 7)
        self.hp += random.randint(5, 10)
        self.defense += random.randint(2, 4)

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
        self.basic_attack(target)

class Goblin(Enemy):
    def __init__(self, level):
        self.name = Fore.RED + "Goblin" + Fore.WHITE
        self.hp = 45 + level
        self.strength = 5 + level
        self.speed = 10
        self.intelligence = 0
        self.defense = 0
        self.max_hp = self.hp
        self.weapon = None
        self.level = level

        self.apply_difficulty()
    
    def rob(self, player):
        if random.random() < 0.50:
            print(Fore.YELLOW + self.name + " attempts to mug " + player.name + " but misses!" + Fore.WHITE)
            print("")
            time.sleep(1)
            return
        if player.money > 0:
            stolen_money = random.randint(1, player.money)
            player.money -= stolen_money
            raw_damage = random.randint(self.strength - 2, self.strength + 2)
            damage = max(1, raw_damage - player.defense)
            player.hp -= damage
            print(self.name + " attempts to rob " + player.name + ", stealing $" + str(stolen_money) + " and dealing " + str(damage) + " damage!")
            print("")
            if player.defense > 0:
                print(Fore.LIGHTBLACK_EX + "(Reduced from " + str(raw_damage) + " by defense)" + Fore.WHITE)
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

    def apply_difficulty(self):
        global difficulty
        if difficulty <= 25:
            self.hp = int(self.hp * 0.9)
            self.strength = int(self.strength * 0.8)
            self.defense = int(self.defense * 0.8)
        elif difficulty <= 50:
            self.hp = int(self.hp * 1.1)
            self.strength = int(self.strength * 1.1)
            self.defense = int(self.defense * 1.05)
        elif difficulty >= 51 and difficulty <= 100:
            self.hp = int(self.hp * 1.2)
            self.strength = int(self.strength * 1.3)
            self.defense = int(self.defense * 1.2)


class CorruptedGoblin(Enemy):
    def __init__(self, level, unstable=False,corrupted=True):
        self.name = Fore.MAGENTA + "Goblin" + Fore.WHITE
        self.real_name = Fore.RED + "Corrupted Goblin" + Fore.WHITE
        self.cleansed_name = Fore.GREEN + "Goblin" + Fore.WHITE
        self.hp = 30 + level
        self.strength = 5 + level
        self.speed = 11
        self.intelligence = 0
        self.defense = 0
        self.max_hp = self.hp
        self.weapon = None
        self.level = level
        self.unstable = unstable
        self.corrupted = corrupted

        if corrupted:
            # Store Non-corrupted Stats
            self.regular_hp = self.hp
            self.regular_strength = self.strength
            self.regular_speed = self.speed
            self.regular_defense = self.defense

            # Buff Enemy
            self.hp += 5 * level
            self.strength += level + 5
            self.speed = self.speed + level
            self.defense += level
            self.max_hp = self.hp

        self.apply_difficulty()

    def rob(self, player):
        if random.random() < 0.50: 
            print(Fore.YELLOW + self.name + " attempts to mug " + player.name + " but misses!" + Fore.WHITE)
            print("")
            time.sleep(1)
            return
        if player.money > 0:
            stolen_money = random.randint(1, player.money)
            player.money -= stolen_money
            raw_damage = random.randint(self.strength - 2, self.strength + 2)
            damage = max(1, raw_damage - player.defense)
            player.hp -= damage
            print(self.name + "twitches violently and steals $" + str(stolen_money) + ", dealing " + str(damage) + " damage!")
            print("")
            if player.defense > 0:
                print(Fore.LIGHTBLACK_EX + "(Reduced from " + str(raw_damage) + " by defense)" + Fore.WHITE)
                print("")
            print(player.name + "'s remaining money: $" + str(player.money))
            print(player.name + " remaining HP: " + str(player.hp))
            print("")
        else:
            print(self.name + " reaches for your pockets... but you have nothing to take.")
            print("")

    def choose_action(self, target):
        if self.unstable == True and random.random() < 0.2:
            print(self.name+ " twitches violently, dealing 5 damage to itself")
            print("")
            self.hp -= 5
            print(self.name + " remaining HP: " + str(self.hp))
            print("")
        if target.money > 0 and random.random() < 0.3:
            self.rob(target)
        else:
            self.basic_attack(target)

    def reveal_identity(self):
        self.name = self.real_name
        print(Fore.YELLOW + "The veil lifts... it's a " + self.real_name + "!" + Fore.WHITE)
        print("")

    def cleanse(self):
        if self.corrupted:
            self.strength = self.regular_strength
            self.hp = self.regular_hp
            self.speed = self.regular_speed
            self.defense = self.regular_defense
            self.unstable = False
            self.corrupted = False

            self.name = self.cleansed_name

    def apply_difficulty(self):
        global difficulty
        if difficulty <= 25:
            self.hp = int(self.hp * 0.9)
            self.strength = int(self.strength * 0.8)
            self.defense = int(self.defense * 0.8)
        elif difficulty <= 50:
            self.hp = int(self.hp * 1.1)
            self.strength = int(self.strength * 1.1)
            self.defense = int(self.defense * 1.05)
        elif difficulty >= 51 and difficulty <= 100:
            self.hp = int(self.hp * 1.2)
            self.strength = int(self.strength * 1.3)
            self.defense = int(self.defense * 1.2)

class Orc(Enemy):
    def __init__(self, level):
        self.name = Fore.MAGENTA + "Orc" + Fore.WHITE
        self.hp = 100 + level
        self.strength = 15 + level
        self.speed = 5
        self.intelligence = 0
        self.defense = 10 + level
        self.max_hp = self.hp
        self.weapon = None
        self.level = level

        self.apply_difficulty()

    def smash(self, player):
        if random.random() < 0.30: 
            print(Fore.YELLOW + self.name + " smashes the ground at " + player.name + " but misses!" + Fore.WHITE)
            print("")
            time.sleep(1)
            return
        raw_damage = calculate_attack(self.strength, 10)
        damage = max(1, raw_damage - player.defense)
        player.hp -= damage
        print(self.name + " smashes " + player.name + " for " + str(damage) + " damage!")
        print("")
        if player.defense > 0:
            print(Fore.LIGHTBLACK_EX + "(Reduced from " + str(raw_damage) + " by defense)" + Fore.WHITE)
            print("")
        print("")
        print(player.name + " remaining HP: " + str(player.hp))
        print("")
        if random.random() < 0.2:
            time.sleep(1)
            player.apply_status('stagger', 1)
    
    def choose_action(self, target):
        if random.random() < 0.5:
            self.smash(target)
        else:
            self.basic_attack(target)

class CorruptedOrc(Enemy):
    def __init__(self, level,unstable=False,corrupted=True):
        self.name = Fore.MAGENTA + "Orc" + Fore.WHITE
        self.real_name = Fore.RED + "Corrupted Orc" + Fore.WHITE
        self.cleansed_name = Fore.GREEN + "Orc" + Fore.WHITE
        self.hp = 100 + level
        self.strength = 15 + level
        self.speed = 5
        self.intelligence = 0
        self.defense = 10 + level
        self.max_hp = self.hp
        self.weapon = None
        self.level = level
        self.unstable = unstable
        self.corrupted = corrupted

        self.apply_difficulty()

        if corrupted:
            # Store Non-corrupted Stats
            self.regular_hp = self.hp
            self.regular_strength = self.strength
            self.regular_speed = self.speed
            self.regular_defense = self.defense

            # Buff Enemy
            self.hp += 5 * level
            self.strength += level + 5
            self.speed = self.speed + level
            self.defense += level
            self.max_hp = self.hp

    def smash(self, player):
        if random.random() < 0.30: 
            print(Fore.YELLOW + self.name + " smashes the ground at " + player.name + " but misses!" + Fore.WHITE)
            print("")
            time.sleep(1)
            return
        raw_damage = calculate_attack(self.strength, 10)
        damage = max(1, raw_damage - player.defense)
        player.hp -= damage
        print(self.name + " smashes " + player.name + " for " + str(damage) + " damage!")
        if player.defense > 0:
            print("")
            print(Fore.LIGHTBLACK_EX + "(Reduced from " + str(raw_damage) + " by defense)" + Fore.WHITE)
        print("")
        print(player.name + " remaining HP: " + str(player.hp))
        print("")
        if random.random() < 0.2:
            time.sleep(1)
            player.apply_status('stagger', 2)

    def choose_action(self, target):
        if self.unstable == True and random.random() < 0.2:
            print(Fore.WHITE+"The Orc growls in pain, giving you a chance for")
            print('an easy attack!')
            print("")
            time.sleep(1)
            return 
        if random.random() < 0.5:
            self.smash(target)
        else:
            self.basic_attack(target)
    
    def cleanse(self):
        if self.corrupted:
            self.strength = self.regular_strength
            self.hp = self.regular_hp
            self.speed = self.regular_speed
            self.defense = self.regular_defense
            self.unstable = False
            self.corrupted = False

            self.name = self.cleansed_name

    def apply_difficulty(self):
        global difficulty
        if difficulty <= 25:
            self.hp = int(self.hp * 0.9)
            self.strength = int(self.strength * 0.8)
            self.defense = int(self.defense * 0.8)
        elif difficulty <= 50:
            self.hp = int(self.hp * 1.1)
            self.strength = int(self.strength * 1.1)
            self.defense = int(self.defense * 1.05)
        elif difficulty >= 51 and difficulty <= 100:
            self.hp = int(self.hp * 1.2)
            self.strength = int(self.strength * 1.3)
            self.defense = int(self.defense * 1.2)


    def reveal_identity(self):
        self.name = self.real_name
        print(Fore.YELLOW + "The veil lifts... it's a " + self.real_name + "!" + Fore.WHITE)
        print("")

    def apply_difficulty(self):
        global difficulty
        if difficulty <= 25:
            self.hp = int(self.hp * 0.9)
            self.strength = int(self.strength * 0.8)
            self.defense = int(self.defense * 0.8)
        elif difficulty <= 50:
            self.hp = int(self.hp * 1.1)
            self.strength = int(self.strength * 1.1)
            self.defense = int(self.defense * 1.05)
        elif difficulty >= 51 and difficulty <= 100:
            self.hp = int(self.hp * 1.2)
            self.strength = int(self.strength * 1.3)
            self.defense = int(self.defense * 1.2)

