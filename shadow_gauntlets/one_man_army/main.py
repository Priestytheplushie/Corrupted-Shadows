from title import title_screen
from discord import connect_to_discord, update_presence, disconnect_from_discord
from text_utils import animate_title, center_text
from discord import update_presence
import time
from player import Player
from enemies import Enemy
from colorama import Fore, Style
import random
from attack import calculate_attack
from item_factory import gauntlet_library, create_item
from inventory import Inventory
from items import *
from battle import enemy_turn
from shadow_gauntlets.grades import *
from strings import *
from title import title_screen
from screens import show_character_sheet

turn = 1
total_turns = 0

# Modifed Player Turn
def player_turn(player, enemies, mode, bonus_ap=0):
    global turn
    status_ticked = False

    ap = 1

    while True:
        if mode == "multi":
            print(Fore.YELLOW + "You have " + str(ap) + " Action Points (AP).")

        if mode == "single" and ap <= 0:
            break  # Exit if no AP left in single mode

        print(Fore.CYAN + "-" * 40)
        typewriter(Fore.MAGENTA + "Your Turn - Turn " + str(turn))

        if mode == "multi":
            print(Fore.WHITE + "HP: " + str(player.hp) + " | Action Points: " + str(ap))

            alive_enemies = [e for e in enemies if e.hp > 0]
            for i, enemy in enumerate(alive_enemies):
                print(Fore.GREEN + str(i + 1) + ". " + enemy.name + " (" + str(enemy.hp) + "/" + str(enemy.max_hp) + " HP)")
        else:
            print(Fore.WHITE + "HP: " + str(player.hp) + " | Enemy HP: " + str(enemies[0].hp) + " | Action Points: " + str(ap))

        print(Fore.CYAN + "-" * 40)
        print("")

        if not status_ticked:
            player.process_status_effects()
            status_ticked = True

        if player.is_staggered():
            print(Fore.YELLOW + player.name + " is staggered and can’t act normally!")
            print("")
            time.sleep(1)
            break

        typewriter(Fore.YELLOW + "What will you do?")

        if ap <= 0 and mode == "multi":
            print(Fore.BLACK + "1. Attack  [Not enough AP]")
            print(Fore.BLACK + "2. Defensive Stance  [Not enough AP]")
            if len(player.inventory.items) > 0:
                print(Fore.BLACK + "3. Use Item  [Not enough AP]")
            print(Fore.BLACK + "4. View Items  [Not enough AP]")
            print(Fore.BLACK + "5. View Character Sheet  [Not enough AP]")
            print(Fore.BLACK + "6. Identify  [Not enough AP]")
        else:
            print(Fore.GREEN + "1. Attack")
            print(Fore.GREEN + "2. Defensive Stance")
            if len(player.inventory.items) > 0:
                print(Fore.GREEN + "3. Use Item")
            print(Fore.GREEN + "4. View Items")
            print(Fore.GREEN + "5. View Character Sheet")
            print(Fore.GREEN + "6. Identify")

        if mode == "multi" or (mode == "single" and enemies[0].hp <= 0):
            print(Fore.GREEN + "7. End Turn")

        choice = input(Fore.YELLOW + "> ").strip().lower()

        if choice == "1":
            if ap > 0:
                if mode == "multi":
                    print(Fore.YELLOW + "Choose a target to attack:")
                    alive_enemies = [e for e in enemies if e.hp > 0]
                    for i, enemy in enumerate(alive_enemies):
                        print(Fore.GREEN + str(i + 1) + ". " + enemy.name + " (" + str(enemy.hp) + "/" + str(enemy.max_hp) + " HP)")
                    try:
                        index = int(input(Fore.YELLOW + "> ")) - 1
                        if 0 <= index < len(alive_enemies):
                            target = alive_enemies[index]
                            if player.weapon is None:
                                player.punch(target)
                            else:
                                if hasattr(player.weapon, 'aoe') and player.weapon.aoe:
                                    print(Fore.YELLOW + "You unleash a powerful area-of-effect attack!")
                                    for enemy in alive_enemies:
                                        if enemy.hp > 0:
                                            player.weapon.attack(player, enemy)
                                else:
                                    player.weapon.attack(player, target)
                            ap -= 1
                        else:
                            print(Fore.RED + "Invalid selection.")
                    except ValueError:
                        print(Fore.RED + "Invalid input.")
                    print("")
                else:
                    target = enemies[0]
                    if target.hp > 0:
                        if player.weapon is None:
                            player.punch(target)
                        else:
                            if hasattr(player.weapon, 'aoe') and player.weapon.aoe:
                                print(Fore.YELLOW + "You unleash a powerful area-of-effect attack!")
                                print("")
                                time.sleep(2)
                                for enemy in enemies:
                                    if enemy.hp > 0:
                                        player.weapon.attack(player, enemy)
                                        time.sleep(2)
                            else:
                                player.weapon.attack(player, target)
                        ap -= 1
                        print("")
                        if ap <= 0:
                            break
            else:
                if mode == "multi":
                    print(Fore.RED + "Not enough Action Points to attack.")

        elif choice == "2":
            if ap > 0:
                player.defend()
                ap -= 1
                if mode == "single" and ap <= 0:
                    break
            else:
                if mode == "multi":
                    print(Fore.RED + "Not enough Action Points to defend.")

        elif choice == "3":
            if len(player.inventory.items) > 0:
                while True:
                    if ap <= 0:
                        print(Fore.RED + "Not enough AP to use an item.")
                        break

                    print(Fore.CYAN + "-" * 40)
                    print(Fore.YELLOW + "Choose an item by number (or 'Enter' to go back):")
                    for i, item in enumerate(player.inventory.items):
                        print(Fore.GREEN + f"{i + 1}. {item.name}")
                        for line in item.description.split("\n"):
                            print(Fore.LIGHTBLACK_EX + "   " + line)
                        if hasattr(item, "durability") and hasattr(item, "max_durability"):
                            print(Fore.LIGHTBLACK_EX + f"   Durability: {item.durability}/{item.max_durability}")
                        elif hasattr(item, "quantity"):
                            print(Fore.LIGHTBLACK_EX + f"   Quantity: {item.quantity}")

                    item_choice = input(Fore.YELLOW + "> ").strip()
                    if item_choice == "":
                        break

                    try:
                        index = int(item_choice) - 1
                        if 0 <= index < len(player.inventory.items):
                            item = player.inventory.items[index]
                            if isinstance(item, UseableItem):
                                print("Choose an enemy to target for cleansing:")
                                for i, enemy in enumerate(enemies):
                                    if enemy.corrupted:
                                        print(Fore.GREEN + f"{i + 1}. {enemy.name}")
                                target_choice = input(Fore.YELLOW + "> ")
                                target = enemies[int(target_choice) - 1]
                                item.use(player, target)
                            elif isinstance(item, Weapon):
                                item.equip(player)
                                print(Fore.GREEN + f"{item.name} equipped!")
                            elif isinstance(item, Potion):
                                item.use(player)
                                print(Fore.GREEN + f"{item.name} used!")
                                player.inventory.items.remove(item)
                            else:
                                print(Fore.RED + "This item cannot be used.")
                            ap -= 1
                            if mode == "single" and ap <= 0:
                                break
                        else:
                            print(Fore.RED + "Invalid item selection.")
                    except ValueError:
                        print(Fore.RED + "Invalid input.")
            else:
                print(Fore.RED + "Your inventory is empty.")

        elif choice == "4":
            for i, item in enumerate(player.inventory.items):
                print(Fore.GREEN + f"{i + 1}. {item.name}")
                for line in item.description.split("\n"):
                    print(Fore.LIGHTBLACK_EX + "   " + line)
                if hasattr(item, "durability") and hasattr(item, "max_durability"):
                    print(Fore.LIGHTBLACK_EX + f"   Durability: {item.durability}/{item.max_durability}")
                elif hasattr(item, "quantity"):
                    print(Fore.LIGHTBLACK_EX + f"   Quantity: {item.quantity}")
            time.sleep(3)

        elif choice == "5":
            show_character_sheet(player, False)

        elif choice == "6":
            if mode == "multi":
                for enemy in enemies:
                    if enemy.hp > 0:
                        print(Fore.CYAN + f"--- Enemy: {enemy.name}")
                        print(Fore.YELLOW + f"Health: {enemy.hp}/{enemy.max_hp}")
                        print(Fore.YELLOW + f"Level: {enemy.level}")
                        if enemy.corrupted:
                            enemy.reveal_identity()
                        time.sleep(1)
            else:
                enemy = enemies[0]
                print(Fore.CYAN + f"--- Enemy: {enemy.name}")
                print(Fore.YELLOW + f"Health: {enemy.hp}/{enemy.max_hp}")
                print(Fore.YELLOW + f"Level: {enemy.level}")
                if enemy.corrupted:
                    enemy.reveal_identity()

        elif choice == "7" and mode == "multi" or (mode == "single" and enemies[0].hp <= 0):
            turn += 1
            break

        else:
            print(Fore.RED + "Invalid input.")

# Modified Battle Script
def battle(player, enemies, battle_mode="single", bonus_ap=-7):
    from discord import update_presence  # Import the update_presence function
    global turn, total_turns
    turn = 1
    total_turns += 1
    clear_screen()
    player_went_first = False

    if not isinstance(enemies, list):
        enemies = [enemies]

    # Update Discord Presence for the start of the battle
    update_presence(
        state="In a Battle (Shadow Gauntlet)",
        details="Preparing for Battle",
        small_image="battle",
        small_text=f"Turn {turn} | Preparing"
    )

    # Battle logic
    if battle_mode == "multi":
        typewriter(random.choice(multi_battle_intro(player, enemies)))
        print("")
        time.sleep(1)
        if all(enemy.speed < player.speed for enemy in enemies):
            typewriter(multi_battle_player_goes_first(player, enemies))
            print("")
            time.sleep(2)
            # Update Discord Presence for player's turn
            update_presence(
                state="In a Battle (Shadow Gauntlet)",
                details=f"Turn {turn} | HP: {player.hp}/{player.max_hp} | AP: {math.ceil(len(enemies) / 2)}",
                small_image="battle",
                small_text=f"Turn {turn} | {player.name}'s Turn"
            )
            player_turn(player, enemies, battle_mode, bonus_ap)
            player_went_first = True
        elif all(enemy.speed > player.speed for enemy in enemies):
            typewriter(multi_battle_enemies_go_first(player, enemies))
            print("")
            time.sleep(1)
            # Update Discord Presence for enemy's turn
            update_presence(
                state="In a Battle",
                details=f"Turn {turn} | Enemies Left: {len([e for e in enemies if e.hp > 0])} | Enemy's Turn",
                small_image="battle",
                small_text=f"Turn {turn} | Enemies' Turn"
            )
            enemy_turn(player, enemies, battle_mode)
        else:
            typewriter(multi_battle_random_initiative(player, enemies))
            print("")
            time.sleep(3)
            if random.choice([True, False]):
                # Update Discord Presence for player's turn
                update_presence(
                    state="In a Battle (Shadow Gauntlet)",
                    details=f"Turn {turn} | HP: {player.hp}/{player.max_hp} | AP: {math.ceil(len(enemies) / 2)}",
                    small_image="battle",
                    small_text=f"Turn {turn} | {player.name}'s Turn"
                )
                player_turn(player, enemies, battle_mode, bonus_ap)
                player_went_first = True
            else:
                # Update Discord Presence for enemy's turn
                update_presence(
                    state="In a Battle (Shadow Gauntlet)",
                    details=f"Turn {turn} | Enemies Left: {len([e for e in enemies if e.hp > 0])} | Enemy's Turn",
                    small_image="battle",
                    small_text=f"Turn {turn} | Enemies' Turn"
                )
                enemy_turn(player, enemies, battle_mode)
    else:
        typewriter(randomized_intro_messages(player, enemies[0]))
        print("")
        time.sleep(2)
        typewriter("Battle started!")
        print("")
        time.sleep(1)
        typewriter(f"{player.name} v.s {enemies[0].name}")
        print("")
        time.sleep(2)
        if enemies[0].speed > player.speed:
            typewriter(enemy_attacks_first_message(player, enemies[0]))
            print("")
            time.sleep(2)
            # Update Discord Presence for enemy's turn
            update_presence(
                state="In a Battle (Shadow Gauntlet)",
                details=f"Turn {turn} | Enemy HP: {enemies[0].hp}/{enemies[0].max_hp} | Enemy's Turn",
                small_image="battle",
                small_text=f"Turn {turn} | Enemies' Turn"
            )
            enemy_turn(player, enemies, battle_mode)
        elif enemies[0].speed < player.speed:
            typewriter(player_attacks_first_message(player, enemies[0]))
            print("")
            time.sleep(1)
            # Update Discord Presence for player's turn
            update_presence(
                state="In a Battle (Shadow Gauntlet)",
                details=f"Turn {turn} | HP: {player.hp}/{player.max_hp} | AP: {1 + bonus_ap}",
                small_image="battle",
                small_text=f"Turn {turn} | {player.name}'s Turn"
            )
            player_turn(player, enemies, battle_mode, bonus_ap)
            player_went_first = True
        else:
            typewriter(random_initiative_message(player, enemies[0]))
            print("")
            time.sleep(3)
            if random.randint(1, 2) == 1:
                # Update Discord Presence for player's turn
                update_presence(
                    state="In a Battle (Shadow Gauntlet)",
                    details=f"Turn {turn} | HP: {player.hp}/{player.max_hp} | AP: {1 + bonus_ap}",
                    small_image="battle",
                    small_text=f"Turn {turn} | {player.name}'s Turn"
                )
                player_turn(player, enemies, battle_mode, bonus_ap)
                player_went_first = True
            else:
                # Update Discord Presence for enemy's turn
                update_presence(
                    state="In a Battle (Shadow Gauntlet)",
                    details=f"Turn {turn} | Enemy HP: {enemies[0].hp}/{enemies[0].max_hp} | Enemy's Turn",
                    small_image="battle",
                    small_text=f"Turn {turn} | Enemies' Turn"
                )
                enemy_turn(player, enemies, battle_mode)

    # Ensure the enemy does not attack twice if they went first
    if not player_went_first and any(e.hp > 0 for e in enemies):
        player_turn(player, enemies, battle_mode, bonus_ap)

    # Main battle loop
    while player.hp > 0 and any(enemy.hp > 0 for enemy in enemies):
        turn += 1
        total_turns += 1
        print("\n" + f"--- Turn {turn} ---")

        # Update Discord Presence during the battle
        if turn % 2 == 1:  # Player's turn
            if battle_mode == "single":
                update_presence(
                    state="In a Battle (Shadow Gauntlet)",
                    details=f"Turn {turn} | HP: {player.hp}/{player.max_hp} | AP: {1 + bonus_ap}",
                    small_image="battle",
                    small_text=f"Turn {turn} | {player.name}'s Turn"
                )
            else:
                update_presence(
                    state="In a Battle (Shadow Gauntlet)",
                    details=f"Turn {turn} | HP: {player.hp}/{player.max_hp} | AP: {math.ceil(len(enemies) / 2)}",
                    small_image="battle",
                    small_text=f"Turn {turn} | {player.name}'s Turn"
                )
            player_turn(player, enemies, battle_mode, bonus_ap)
        else:  # Enemy's turn
            if battle_mode == "single":
                update_presence(
                    state="In a Battle",
                    details=f"Turn {turn} | Enemy HP: {enemies[0].hp}/{enemies[0].max_hp} | Enemy's Turn",
                    small_image="battle",
                    small_text=f"Turn {turn} | Enemies' Turn"
                )
            else:
                update_presence(
                    state="In a Battle",
                    details=f"Turn {turn} | Enemies Left: {len([e for e in enemies if e.hp > 0])} | Enemy's Turn",
                    small_image="battle",
                    small_text=f"Turn {turn} | Enemies' Turn"
                )
            enemy_turn(player, enemies, battle_mode)

    if player.hp <= 0:
        return False
    else:
        return True

gauntlet_library.update({
    "Double Axe": {
        "type": "aoe_weapon",
        "description": (
            "A devastating axe with two sharp blades, fit \n"
            "for the most barbaric fighters \n"
            "Damage: +30"
        ),
        "damage": 50,
        "durability": 100
    },
    "Insane Health Potion": {
        "type": "potion",
        "description": (
            "This mystical brew is insanely potent! When \n"
            "consumed, it restores 300 HP"
        ),
        "healing_amount": 300,
        "quantity": 1
    }
})


class ShadowRaider(Enemy):
    def __init__(self, level,unstable=False,corrupted=False):
        self.name = Fore.MAGENTA + "Corrupted Raider" + Fore.WHITE
        self.real_name = Fore.RED + "Corrupted Raider" + Fore.WHITE
        self.cleansed_name = Fore.GREEN + "Raider" + Fore.WHITE
        self.hp = random.randint(125,200)
        self.strength = 15
        self.speed = 3
        self.intelligence = 100
        self.defense = 0
        self.max_hp = self.hp
        self.status_effects = []  
        self.weapon = None
        self.loot_table_key = "none"
        self.level = level
        self.unstable = unstable
        self.corrupted = corrupted
    
    def swift_strike(self, player):
        if random.random() < 0.50: 
            print(Fore.YELLOW + self.name + " attempts to rush at " + player.name + " but misses!" + Fore.WHITE)
            print("")
            time.sleep(1)
            return
        raw_damage = calculate_attack(self.strength, 5)
        damage = max(1, raw_damage - player.defense)
        player.hp -= damage
        print(self.name + " strikes " + player.name + " for " + str(damage) + " damage!")
        if player.defense > 0:
            print("")
            print(Fore.LIGHTBLACK_EX + "(Reduced from " + str(raw_damage) + " by defense)" + Fore.WHITE)
        print("")
        print(player.name + " remaining HP: " + str(player.hp))
        print("")
    
    def shadow_strike(self, player):
        if random.random() < 0.75: 
            print(Fore.YELLOW + self.name + " tries to hide from " + player.name + " but fails!" + Fore.WHITE)
            print("")
            time.sleep(1)
            return
        raw_damage = calculate_attack(self.strength, 5)
        damage = max(1, raw_damage - player.defense)
        player.hp -= damage
        print(self.name + " strikes " + player.name + " from the shadows for " + str(damage) + " damage!")
        if player.defense > 0:
            print("")
            print(Fore.LIGHTBLACK_EX + "(Reduced from " + str(raw_damage) + " by defense)" + Fore.WHITE)
        print("")
        print(player.name + " remaining HP: " + str(player.hp))
        print("")
    
    def choose_action(self, target):
        if random.random() < 0.3:
            self.swift_strike(target)
        elif random.random() < 0.3:
            self.shadow_strike(target)
        else:
            self.basic_attack(target)

def display_results(grade, player, win):
    global total_turns  # Using global turn count

    # Define colors based on the grade
    grade_colors = {
        'A': Fore.GREEN,
        'B': Fore.BLUE,
        'C': Fore.WHITE,
        'D': Fore.MAGENTA,
        'F': Fore.RED
    }

    # Choose a message based on the grade
    if grade == 'A':
        message = random.choice(A_message)
    elif grade == 'B':
        message = random.choice(B_message)
    elif grade == 'C':
        message = random.choice(C_message)
    elif grade == 'D':
        message = random.choice(D_message)
    else:
        message = random.choice(F_message)

    result_color = Fore.GREEN if win else Fore.RED
    result_text = "Victory!" if win else "Defeat..."

    print("-" * 40)
    if win == False:
        print(result_color + "Gauntlet Failed!" + Style.RESET_ALL)
    else:
        print(result_color + "Gauntlet Complete!" + Style.RESET_ALL)
    print("-" * 40)
    print(result_color + "Result: " + result_text + Style.RESET_ALL)
    print("-" * 40)
    print(grade_colors.get(grade, Fore.WHITE) + "Grade: " + grade + Style.RESET_ALL)
    print("-" * 40)
    print("Turns Taken: " + str(total_turns))
    print("HP Remaining: " + str(player.hp) + "/" + str(player.max_hp))
    print("-" * 40)
    print(grade_colors.get(grade, Fore.WHITE) + "" + message + Style.RESET_ALL)
    print("-" * 40)
    input = input(Fore.YELLOW+"Press any key to return to Title Screen")

grade = "F" # Start at a F

def start_gauntlet():
    global grade
    clear_screen()
    update_presence("Shadow Gauntlet - One Man Army", "Alone Against the Horde")
    animate_title(Fore.MAGENTA+"Shadow Gauntlet"+Fore.WHITE+" - "+Fore.GREEN+"One Man Army")
    time.sleep(1)
    typewriter(Fore.YELLOW + "What is your name?", delay=0.03)
    name = input(Fore.CYAN + "> ")
    clear_screen()

    # Intro
    typewriter(Fore.WHITE+"You stand alone at the gates of your village. The raiders are coming...")
    typewriter("under the cover of darkness, sneaking from the shadows! If you fall...")
    typewriter("the village is doomed!")
    print("")

    # Create Objects
    weapon = create_item("Double Axe")


    # Create Premade Character
    player = Player(name,300,23,50,100,0,0,None,50)
    player.inventory.add_item(weapon)
    player.equip_weapon(weapon,False)
    player.inventory.add_item(create_item("Insane Health Potion"))
    player.inventory.add_item(create_item("Insane Health Potion"))

    # Create Raiders
    raider_1 = ShadowRaider(5)
    raider_2 = ShadowRaider(5)
    raider_3 = ShadowRaider(5)
    raider_4 = ShadowRaider(5)
    raider_5 = ShadowRaider(5)
    raider_6 = ShadowRaider(5)
    raider_7 = ShadowRaider(5)
    raider_8 = ShadowRaider(5)
    raider_9 = ShadowRaider(5)
    raider_10 = ShadowRaider(5)

    enemies = [raider_1,raider_2,raider_3,raider_4,raider_5,raider_6,raider_7,raider_8,raider_9,raider_10]

    typewriter(Fore.WHITE + "You're alone and afraid, the shadows of war are closing in, and")
    typewriter("you're a one-man army... and the horde is rushing in!")
    print("")
    typewriter("Raiders from the shadows emerge, ready to raid the only place you have left.")
    typewriter("It's you versus the world, so get to it!")
    print("")
    time.sleep(1)

    # Battle begins
    result = battle(player, enemies, "multi")
    clear_screen()
    update_presence("Shadow Gauntlet - One Man Army", "Alone Against the Horde")
    time.sleep(1)

    if result == False:
        grade = "F"
        display_results(grade,player,False)

    # Wave #2
    typewriter(Fore.WHITE+"The raiders lie defeated, but more are coming! The onslaught is endless!")
    print("")
    time.sleep(1)
    typewriter("You hear distant screams coming from behind you! Villagers are running, It's chaos! If")
    typewriter("you fall now, it's all over!")
    print("")
    time.sleep(1)

    # Reset Enemies
    raider_1 = ShadowRaider(5)
    raider_2 = ShadowRaider(5)
    raider_3 = ShadowRaider(5)
    raider_4 = ShadowRaider(5)
    raider_5 = ShadowRaider(5)
    raider_6 = ShadowRaider(5)
    raider_7 = ShadowRaider(5)
    raider_8 = ShadowRaider(5)
    raider_9 = ShadowRaider(5)
    raider_10 = ShadowRaider(5)

    enemies = [raider_1,raider_2,raider_3,raider_4,raider_5,raider_6,raider_7,raider_8,raider_9,raider_10]

    result = battle(player, enemies, "multi")
    update_presence("Shadow Gauntlet - One Man Army", "Alone Against the Horde")
    clear_screen()
    time.sleep(1)

    if result == False:
        grade = "F"
        display_results(grade,player,False)

    # After the battle
    typewriter(Fore.WHITE + "The raiders retreat, slinking back into the shadows.")
    typewriter("You rise to your feet, observing the aftermath. The village is saved.")
    typewriter("Your one-man army prevailed.")

    display_results(grade,player,result)
    title_screen()