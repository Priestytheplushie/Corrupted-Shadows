import time
import random
import sys
from player import Player
from text_utils import *
from utils import heal_player_precent
from tower.tower_data import floor, tower_difficulty, tower_score, next_battle, bonus_ap
from tower.tower_battle import battle
from tower.tower_enemies import *
from tower.tower_item_data import tower_library
from item_factory import create_item
from tower.tower_screens import *
from screens import show_character_sheet
from discord import update_presence
import threading

enemies = []

def setup_next_battle(player):
    global floor, tower_difficulty, tower_score, next_battle, enemies
    difficulty_multipliers = {
        "easy": 0.5,
        "normal": 1.0,
        "hard": 1.5,
        "hardcore": 2
    }
    multiplier = difficulty_multipliers.get(tower_difficulty, 1.0)
    max_enemies = int(floor * multiplier)

    # Ensure that the number of enemies is at least 2
    max_enemies = max(2, max_enemies)

    amount = random.randint(2, max_enemies)
    amount = min(amount, 6)  # Ensure no more than 6 enemies

    # Randomize Enemies
    enemy_types = [
        CorruptedHuman,
        CorruptedWarrior,
        CorruptedMage
    ]

    enemies = []

    if next_battle == "single":
        enemy_type = random.choice(enemy_types)
        enemy = enemy_type(level=floor)
        enemies = [enemy]
        # Adjust tower score for single battle
        tower_score = floor + enemy.level
    elif next_battle == "multi":
        for _ in range(amount):
            enemy_type = random.choice(enemy_types)
            enemy = enemy_type(level=floor)
            enemies.append(enemy)
        # Adjust tower score for multi battle
        tower_score = floor + sum(enemy.level for enemy in enemies)

def present_battle_info(player):
    global enemies, bonus_ap
    update_presence(
        state=f"Tower - Pre Battle ({floor})",
        details=f"Next Battle: {next_battle.capitalize()} | Score: {tower_score}",
    )
    while True:
        clear_screen()

        # Display Player Info
        print(Fore.YELLOW + "Player Info:" + Style.RESET_ALL)
        weapon = player.weapon.name if player.weapon else "None"
        durability = player.weapon.durability if player.weapon else "N/A"
        print(Fore.CYAN + f"- Name: {player.name}" + Style.RESET_ALL)
        print(Fore.CYAN + f"- HP: {player.hp}/{player.max_hp}" + Style.RESET_ALL)
        print(Fore.CYAN + f"- Weapon: {weapon} (Durability: {durability})" + Style.RESET_ALL)
        print(Fore.CYAN + f"- Bonus AP: {bonus_ap}" + Style.RESET_ALL)
        print("")

        # Display Enemies
        print(Fore.YELLOW + "Enemies you must face this battle:" + Style.RESET_ALL)
        for enemy in enemies:
            print(Fore.CYAN + f"- {enemy.name} (Level {enemy.level})" + Style.RESET_ALL)  # Changed to enemy.name
        print("")

        # Menu Options
        print(Fore.CYAN + "What would you like to do?")
        print("[1] Ready Up")
        print("[2] Check Inventory")
        print("[3] View Character Sheet")
        if player.battle_shifter:
            print("[4] Use Battle Shifter (Re-roll the battle)")

        choice = input(Fore.YELLOW + "Choose an option: " + Style.RESET_ALL).strip()

        if choice == "1":
            print(Fore.GREEN + "You ready yourself for the battle!" + Style.RESET_ALL)
            time.sleep(1)
            break  # Exit the loop and proceed to the battle
        elif choice == "2":
            player.inventory.use_non_combat_item(player)
        elif choice == "3":
            show_character_sheet(player)
        elif choice == "4" and player.battle_shifter:
            print(Fore.GREEN + "Using the Battle Shifter to re-roll the battle..." + Style.RESET_ALL)
            player.battle_shifter = False  # Mark the Battle Shifter as used
            setup_next_battle(player)  # Re-roll the battle
            time.sleep(1)
        else:
            print(Fore.RED + "Invalid choice. Please select a valid option." + Style.RESET_ALL)
            time.sleep(1)

    return True  # Indicate that the player is ready for the battle

def calculate_reward(player):
    global floor, tower_difficulty, tower_score, next_battle, enemies, bonus_ap

    # Initialize reroll and battle shifter attributes if not already set
    if not hasattr(player, 'reroll_used'):
        player.reroll_used = 0
    if not hasattr(player, 'battle_shifter'):
        player.battle_shifter = False

    # Generate reward options
    all_items = list(tower_library.keys())
    item_choices = random.sample(all_items, 2)

    stat_boosts = ["HP", "Strength", "Defense", "Intelligence", "Speed", "AP", "Healing"]
    stat_boost_type = random.choice(stat_boosts)
    stat_boost_amount = 1 if stat_boost_type == "AP" else random.randint(5, 15)
    healing_percent = random.randint(25, 50) if stat_boost_type == "Healing" else 0
    battle_shifter = random.random() < 0.33

    # Determine the third reward description
    if battle_shifter:
        third_reward = "Battle Shifter"
    elif stat_boost_type == "Healing":
        third_reward = f"Healing Boost ({healing_percent}% HP)"
    else:
        third_reward = f"{stat_boost_type} Boost (+{stat_boost_amount})"

    # Rewards to cycle through
    rewards = [
        f"1/3 - {item_choices[0]}",
        f"2/3 - {item_choices[1]}",
        f"3/3 - {third_reward}"
    ]

    # Flag to stop the Rich Presence thread
    stop_rich_presence = threading.Event()

    # Function to update Rich Presence in a separate thread
    def update_rich_presence():
        while not stop_rich_presence.is_set():
            for i in range(len(rewards)):
                if stop_rich_presence.is_set():
                    break
                update_presence(
                    state=f"Tower - Floor {floor} | Reward Selection",
                    details=rewards[i]
                )
                time.sleep(1.5)

    # Start the Rich Presence thread
    rich_presence_thread = threading.Thread(target=update_rich_presence)
    rich_presence_thread.start()

    # Display reward selection screen
    clear_screen()
    print(Fore.YELLOW + Style.BRIGHT + "╔" + "═" * 58 + "╗")
    print("║{:^58}║".format("TOWER REWARD SELECTION"))
    print("╠" + "═" * 58 + "╣")

    print("║  [1] " + Fore.GREEN + "{:<52}".format(item_choices[0]) + Style.RESET_ALL + "║")
    for line in tower_library[item_choices[0]]["description"].split("\n"):
        print("║      " + Fore.WHITE + line.ljust(52) + Style.RESET_ALL + "║")
    print("╠" + "─" * 58 + "╣")

    print("║  [2] " + Fore.GREEN + "{:<52}".format(item_choices[1]) + Style.RESET_ALL + "║")
    for line in tower_library[item_choices[1]]["description"].split("\n"):
        print("║      " + Fore.WHITE + line.ljust(52) + Style.RESET_ALL + "║")
    print("╠" + "─" * 58 + "╣")

    if battle_shifter:
        print("║  [3] Battle Shifter - Re-roll the next battle         ║")
    elif stat_boost_type == "Healing":
        print("║  [3] Healing Boost - Restore {:>3}% of HP              ║".format(healing_percent))
    else:
        print("║  [3] {0} Boost - +{1} {0:<40}║".format(stat_boost_type, stat_boost_amount))

    if player.reroll_used == 0:
        print("╠" + "─" * 58 + "╣")
        print("║  [4] Re-roll rewards (one-time use)                   ║")

    print("╚" + "═" * 58 + "╝" + Style.RESET_ALL)

    selected_reward = None

    # Handle player choice
    while True:
        choice = input(Fore.CYAN + "Enter your choice (1-4): " + Style.RESET_ALL).strip()

        if choice == "1":
            item = create_item(item_choices[0])
            if item:
                player.inventory.add_item(item)
                selected_reward = item_choices[0]
                print(Fore.GREEN + "You received: " + item_choices[0] + "!" + Style.RESET_ALL)
            break
        elif choice == "2":
            item = create_item(item_choices[1])
            if item:
                player.inventory.add_item(item)
                selected_reward = item_choices[1]
                print(Fore.GREEN + "You received: " + item_choices[1] + "!" + Style.RESET_ALL)
            break
        elif choice == "3":
            if battle_shifter:
                player.battle_shifter = True
                selected_reward = "Battle Shifter"
                print(Fore.GREEN + "You received the Battle Shifter!" + Style.RESET_ALL)
            elif stat_boost_type == "Healing":
                heal_player_precent(player, healing_percent)
                selected_reward = f"Healing Boost ({healing_percent}% HP)"
                print(Fore.GREEN + f"You recovered {healing_percent}% of your max HP!" + Style.RESET_ALL)
            else:
                if stat_boost_type == "HP":
                    player.hp += stat_boost_amount
                elif stat_boost_type == "Strength":
                    player.strength += stat_boost_amount
                elif stat_boost_type == "Defense":
                    player.defense += stat_boost_amount
                elif stat_boost_type == "Intelligence":
                    player.intelligence += stat_boost_amount
                elif stat_boost_type == "Speed":
                    player.speed += stat_boost_amount
                elif stat_boost_type == "AP":
                    bonus_ap += 1
                selected_reward = f"{stat_boost_type} Boost (+{stat_boost_amount})"
                print(Fore.GREEN + f"Your {stat_boost_type} increased by {stat_boost_amount}!" + Style.RESET_ALL)
            break
        elif choice == "4" and player.reroll_used == 0:
            print(Fore.YELLOW + "\nRe-rolling rewards..." + Style.RESET_ALL)
            player.reroll_used += 1
            time.sleep(1)
            stop_rich_presence.set()  # Stop the current Rich Presence thread
            rich_presence_thread.join()  # Ensure the thread stops before restarting
            calculate_reward(player)  # Restart the reward selection process
            return  # Exit the current function after re-rolling
        elif choice == "4" and player.reroll_used > 0:
            print(Fore.RED + "You have already used your re-roll!" + Style.RESET_ALL)
        else:
            print(Fore.RED + "Invalid choice. Please select 1, 2, 3, or 4." + Style.RESET_ALL)

    # Stop the Rich Presence thread
    stop_rich_presence.set()
    rich_presence_thread.join()

    # Update Rich Presence to show the selected reward
    update_presence(
        state=f"Tower - Floor {floor}",
        details=f"Selected Reward: {selected_reward}"
    )

    time.sleep(2)

def floor_screen(player, increase_floor=True,first_call=False):
    from colorama import Fore, Style

    global floor, tower_score, tower_difficulty, next_battle

    if increase_floor:
        floor += 1

    if first_call:
        if floor == 1:
            next_battle = "single"
        else:
            battle_types = ["single", "multi"]
            next_battle = random.choice(battle_types)
            
    # Corruption Bar
    corruption_percent = min(max(player.corruption, 0), 100)
    bar_length = 10
    filled_length = int(bar_length * corruption_percent / 100)
    bar = Fore.MAGENTA + "█" * filled_length + Fore.WHITE + "░" * (bar_length - filled_length)

    print(Fore.MAGENTA + "╔" + "═" * 58 + "╗")
    print(Fore.CYAN + "║" + f"  TOWER FLOOR {str(floor).rjust(2)}".center(58) + "║")
    print(Fore.MAGENTA + "╠" + "═" * 58 + "╣")

    line = ""
    line += Fore.YELLOW + " Score: " + Fore.WHITE + str(tower_score).ljust(8)
    line += Fore.YELLOW + "Next: " + Fore.GREEN + next_battle.capitalize().ljust(10)
    line += Fore.RED + "HP: " + Fore.WHITE + (str(player.hp) + "/" + str(player.max_hp)).ljust(9)
    print("║" + line.ljust(58) + "║")

    print(Fore.CYAN + "║" + Fore.MAGENTA + " Corruption: [" + bar + Fore.MAGENTA + "]".ljust(56) + "║")
    print(Fore.MAGENTA + "╠" + "═" * 58 + "╣")

    options = [
        "[1] Start Next Battle",
        "[2] View Character Sheet",
        "[3] Check Inventory",
        "[4] Give Up"
    ]

    for option in options:
        print(Fore.CYAN + "║   " + option.ljust(52) + "║")

    print(Fore.MAGENTA + "╚" + "═" * 58 + "╝" + Style.RESET_ALL)

def main(player):
    global floor, tower_difficulty, tower_score, next_battle, enemies, bonus_ap

    # Intro
    clear_screen()
    intro_lines = [
        Fore.WHITE + "You stand before a massive tower, but something seems",
        "off from inside. You see purple flames and other strange",
        "effects escaping from the door. You feel terrified, but",
        "press on. Rumors have it treasure awaits atop the tower..."
    ]
    for line in intro_lines:
        typewriter(line)
    time.sleep(2)

    print("")

    # Starting Equipment
    player.inventory.add_item(create_item("Health Potion"))
    wooden_sword = create_item("Wooden Sword")
    player.inventory.add_item(wooden_sword)
    player.equip_weapon(wooden_sword,True)

    # Tower Loop
    while True:
        clear_screen()
        floor_screen(player, False,True)
        update_presence(
        state=f"Tower - Floor {floor}",
        details=f"Next Battle: {next_battle.capitalize()} | Score: {tower_score}",
        )
        player.reroll_used = 0
        choice = input(Fore.CYAN + Style.BRIGHT + "Choose an option > ").strip()
        while choice not in ["1", "2", "3", "4"]:
            typewriter(Fore.RED + "Invalid selection. Please choose a valid option.", delay=0.03)
            print("")
            choice = input(Fore.CYAN + "Choose an option > ").strip()

        if choice == "1":
            # Store the current score before the battle
            previous_score = tower_score

            setup_next_battle(player)
            present_battle_info(player)  # Display enemies and allow preparation
            top_score = tower_score
            tower_score = previous_score
            result = battle(player, enemies, next_battle, bonus_ap)

            if result is False:

                if tower_difficulty == "hardcore":
                    death_screen()
                    break
                else:
                    player.corruption += 10
                    if player.corruption >= 100:
                        corrupted_death_screen()
                    else:
                        print("")
                        typewriter(Fore.MAGENTA + "You feel the corruption inside you worsen...")
                        typewriter("You've got to find a cure before it's too late!\n")
                        typewriter(Fore.MAGENTA + "Current Corruption: " + str(player.corruption) + "%")
                        display_corruption_bar(player)

                    heal_player_precent(player, 10)
                    time.sleep(2)
                    typewriter(Fore.RED + "You have been defeated! You must try again.")
                    print("")
                    input(Fore.YELLOW + Style.BRIGHT + "Press Enter to try again...")
                    continue

            elif result is True:
                tower_score = top_score
                calculate_reward(player)

            heal_player_precent(player, 10)

            clear_screen()
            print(Fore.GREEN + Style.BRIGHT + "=== Floor Cleared ===\n")
            print(Fore.WHITE + "Floor:".ljust(20) + str(floor))
            print("Tower Difficulty:".ljust(20) + tower_difficulty.capitalize())
            print("Tower Score:".ljust(20) + str(tower_score))
            print("Current HP:".ljust(20) + f"{player.hp}/{player.max_hp} (Recovered 10%)")

            # Update Discord Rich Presence for Floor Cleared Summary
            update_presence(
                state="Ascending the Tower",
                details=f"Floor {floor} | Score {tower_score} | HP {player.hp}/{player.max_hp}"
            )

            if tower_difficulty != "hardcore":
                print("Corruption:".ljust(20) + f"{player.corruption}%")
                display_corruption_bar(player)

            print("")
            input(Fore.YELLOW + Style.BRIGHT + "Press Enter to continue to the next floor...")
            floor += 1

        elif choice == "2":
            show_character_sheet(player)
            time.sleep(1)
            floor_screen(player, False)

        elif choice == "3":
            player.inventory.use_non_combat_item(player)
            time.sleep(1)
            floor_screen(player, False)

        elif choice == "4":
            typewriter(Fore.RED + "Are you sure you want to give up?")
            typewriter("You won't be able to return to this Tower Run.")
            confirm = input(Fore.CYAN + "Type 'yes' to confirm, or anything else to cancel > ").strip().lower()
            if confirm == "yes":
                give_up_screen()