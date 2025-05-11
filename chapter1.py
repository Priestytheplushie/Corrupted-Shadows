# Imports
import time
import random
import cmd
import sys
import textwrap
from player import Player
from title import title_screen
from new_game import character_creation
from enemies import *
from battle import *
from items import *
from item_factory import create_item
from game_data import *
from utils import *
from discord import connect_to_discord, update_presence, disconnect_from_discord

# Color Coding

# White = Normal Text
# Yellow = Event, Important Term, Player Action
# Green = The Player
# Red = The enemy / Fail Requirement
# Purple = Special Event / Occasion

# Blue = Speed Check 
# Cyan = Intelligence Check 
# Light Red = Strength Check

def chapter_1(player):
    global chapter, act
    # Clear 
    clear_screen()

    # Update Discord Status
    update_presence(
        state="Playing Campaign",
        details="Chapter 1 - The Corruption",
        large_image="corrupted_shadows",
        large_text="Corrupted Shadows",
        small_image="corrupted_book",
        small_text=f"{player.name} | HP: {player.hp}/{player.max_hp} | Lvl: {player.level} | Chapter {chapter} - Act {act}"
    )
    
    # Title Card
    animate_title(Fore.MAGENTA+"Chapter 1 - The Corruption")
    time.sleep(3)
    clear_screen()

    # Assign Starting Equipment
    iron_sword = create_item("Iron Sword")
    potion = create_item("Health Potion")
    potion2 = create_item("Health Potion")
    potion3 = create_item("Health Potion")

    player.inventory.add_item(iron_sword)
    player.equip_weapon(iron_sword,True)

    # 3 Health Potions
    player.inventory.add_item(potion)
    player.inventory.add_item(potion2)
    player.inventory.add_item(potion3)

    # Chapter Structure
    intro(player)
    village_result = the_village(player)
    the_forest(player, village_result)
    ap_bonus = goblin_camp(player)
    encounter_result = timed_encounter(player,ap_bonus)
    ending(player, encounter_result)

    # Extras
    chapter = 1
    act = 1

def intro(player):
    # Update Discord Rich Presence
    update_presence(
        state="Playing Campaign",
        details="Chapter 1 - Prelude",
        large_image="corrupted_shadows",
        large_text="Corrupted Shadows",
        small_image="corrupted_book",
        small_text=f"{player.name} | HP: {player.hp}/{player.max_hp} | Lvl: {player.level} | Chapter {chapter} - Act {act}"
    )
    # Background
    typewriter(Fore.WHITE + "50 years after the" + Fore.MAGENTA + " Great War" + Fore.WHITE + ", the world was slowly healing")
    typewriter("from the scars of battle, but one day... everything changed.")
    print("")
    time.sleep(2)
    typewriter("Rumors spread from village to village, of" + Fore.RED + " strange occurrences")
    typewriter(Fore.WHITE + "happening throughout the land.")
    print("")
    time.sleep(1)
    typewriter(Fore.WHITE + "Whispers of a" + Fore.MAGENTA + " corruption" + Fore.WHITE + " rising from the shadows...")
    typewriter("The world, once at peace, now finds itself in chaos.")
    print("")
    time.sleep(2)
    typewriter(Fore.RED + "The world would never be the same again...")
    print("")
    time.sleep(3)
    clear_screen()
    animate_title(Fore.GREEN+"Act I - The Village")
    update_presence(
        state="Playing Campaign",
        details="Chapter 1 - Act 1",
        large_image="corrupted_shadows",
        large_text="Corrupted Shadows",
        small_image="corrupted_book",
        small_text=f"{player.name} | HP: {player.hp}/{player.max_hp} | Lvl: {player.level} | Chapter 1 - Act 1"
    )
    clear_screen()
    typewriter(Fore.RED+"You awaken with a shake! The skies have turned to darkness,")
    typewriter("goblins are running rampant, but something is very wrong here...")
    print("")
    time.sleep(1)
    typewriter(Fore.WHITE + "You look out your window. The village you swore to protect")
    typewriter("is under siege! You've got to get out there and do something!")
    print("")
    time.sleep(3)

def the_village(player):
    # Create Enemies
    corrupted_goblin = CorruptedGoblin(1)

    # Story
    typewriter(Fore.WHITE + "You run outside, watching as the once peaceful village is being raided")
    typewriter("by goblins, but you notice some strange oddities about them.")
    print("")
    time.sleep(1)
    typewriter(Fore.WHITE + "As you approach, you can hear the helpless cries of the villagers and the")
    typewriter("evil laughter of the goblins. Chaos surrounds you as you are forced to make")
    typewriter("a choice...")
    print("")
    time.sleep(3)
    print("\n" + Fore.CYAN + "=" * 50)
    print(Fore.YELLOW + " What will you do?".center(50))
    print(Fore.CYAN + "=" * 50)

    if player.speed >= 10:
        print(Fore.GREEN + " [1] ".ljust(6) + "Protect the Village")
        print(Fore.GREEN + " [2] ".ljust(6) + "Run Away", Fore.BLUE + "(Speed: 10)")
    else:
        print(Fore.GREEN + " [1] ".ljust(6) + "Protect the Village")
        print(Fore.GREEN + " [2] ".ljust(6) + "Run Away", Fore.RED + "(Speed: 10)")
    print(Fore.YELLOW + " [3] ".ljust(6) + "Check Inventory")
    print(Fore.CYAN + "=" * 50)
    print(Fore.BLUE + "Your Speed:", player.speed)
    print(Fore.CYAN + "=" * 50)
    while True:
        choice = input(Fore.YELLOW + "> ").strip()
        if choice == "1":
            typewriter(Fore.BLUE + "You charge at the invading goblin, still maintaining courage")
            typewriter("after all these years of peace.")
            print("")
            time.sleep(1)
            battle(player, corrupted_goblin,"single")
            update_presence("Playing Campagin", "Chapter 1 Act 1")
            break
        elif choice == "2":
            # Branch to "The Escape"
            if player.speed >= 10:
                typewriter(Fore.WHITE + "You slowly back away, avoiding combat and slipping")
                typewriter(Fore.WHITE + "into the shadows...")
                print("")
                time.sleep(2)
                typewriter(Fore.WHITE + "As you leave the village, you hear the helpless cries")
                typewriter("of the villagers you left behind..." + Fore.MAGENTA + " Did you make the right choice?")
                print("")
                time.sleep(3)
                typewriter(Fore.WHITE + "The village is claimed by the goblins! You run off")
                typewriter("towards the forest, leaving your" + Fore.RED + " past behind...")
                print("")
                time.sleep(2)
                typewriter(Fore.WHITE + "You look back one last time with tears in your eyes. The")
                typewriter("village you've lived in for years is gone, and now you're on your own.")
                print("")
                time.sleep(3)
                return "flee"
            else:
                typewriter(Fore.WHITE + "You attempt to flee, but the goblin quickly reacts, blocking")
                typewriter("your path! You're not leaving without a fight!")
                print("")
                time.sleep(1)
                battle(player, corrupted_goblin,"single")
                update_presence("Playing Campagin", "Chapter 1 Act 1")
                break
        elif choice == "3":
            player.inventory.use_non_combat_item(player)
            time.sleep(1)
            print("\n" + Fore.CYAN + "=" * 50)
            print(Fore.YELLOW + " What will you do?".center(50))
            print(Fore.CYAN + "=" * 50)

            if player.speed > 10:
                print(Fore.GREEN + " [1] ".ljust(6) + "Protect the Village")
                print(Fore.GREEN + " [2] ".ljust(6) + "Run Away", Fore.BLUE + "(Speed: 10)")
            else:
                print(Fore.GREEN + " [1] ".ljust(6) + "Protect the Village")
                print(Fore.GREEN + " [2] ".ljust(6) + "Run Away", Fore.RED + "(Speed: 10)")
            print(Fore.YELLOW + " [3] ".ljust(6) + "Check Inventory")
            print(Fore.CYAN + "=" * 50)
            print(Fore.BLUE + "Your Speed:", player.speed)
            print(Fore.CYAN + "=" * 50)

        else:
            print(Fore.RED + "Please choose a valid option!")
            print("")

    # After Battle #1
    typewriter(Fore.GREEN + "The goblin lies defeated!" + Fore.WHITE + " But that")
    typewriter("was only one of the many invaders...")
    print("")
    time.sleep(2)
    typewriter(Fore.WHITE + "You notice the goblin shaking on the floor, bouncing between")
    typewriter("life and death in an instant.")
    print("")
    time.sleep(3)
    print(Fore.YELLOW + "What will you do?".center(50))
    print(Fore.CYAN + "=" * 50)
    print(Fore.GREEN + " [1] ".ljust(6) + "Investigate the Goblin")
    print(Fore.GREEN + " [2] ".ljust(6) + "Locate Villagers")
    print(Fore.YELLOW + " [3] ".ljust(6) + "Check Inventory")
    print(Fore.CYAN + "=" * 50)
    while True:
        choice = input(Fore.YELLOW + "> ").strip()
        if choice == "1":
            typewriter(Fore.WHITE + "You approach the goblin and look at it. It whispers")
            typewriter('in a soft voice:' + Fore.RED + ' "The corruption will consume us all"')
            print("")
            time.sleep(1)
            typewriter(Fore.WHITE + "Before you can react, the goblin appears lifeless")
            typewriter("on the ground...")
            print("")
            time.sleep(2)
            typewriter(Fore.WHITE+"While you were distracted, the goblins finished ravaging the once")
            typewriter("peaceful village. You feel a sense of sadness and sorrow, but")
            typewriter("you seem to be more curious about the strange goblin.")
            print("")
            time.sleep(2)
            break
        elif choice == "2":
            typewriter(Fore.WHITE + "As you search the village for survivors, you find")
            typewriter("none standing... This once cheerful village has fallen, and it's")
            typewriter("time to make your leave...")
            print("")
            time.sleep(3)
            break
        elif choice == "3":
            player.inventory.use_non_combat_item(player)
            time.sleep(1)
            print("\n" + Fore.CYAN + "=" * 50)
            print(Fore.YELLOW + " What will you do?".center(50))
            print(Fore.CYAN + "=" * 50)
            print(Fore.GREEN + " [1] ".ljust(6) + "Investigate the Goblin")
            print(Fore.GREEN + " [2] ".ljust(6) + "Locate Villagers")
            print(Fore.YELLOW + " [3] ".ljust(6) + "Check Inventory")
            print(Fore.CYAN + "=" * 50)

    typewriter(Fore.WHITE + "As you leave the village you keep thinking")
    typewriter("to yourself..." + Fore.MAGENTA + " What was motivating those goblins?")
    print("")
    typewriter(Fore.WHITE + "You watched as they ignored all the gold and other")
    typewriter("valuables, and went straight for the kill.")
    print("")
    typewriter(Fore.WHITE + "But you have no time to dwell on that... As you must cross")
    typewriter("through the dense forest in order to reach" + Fore.GREEN + " The Iron Fist.")
    print("")
    time.sleep(3)
    return "fight"

def the_forest(player, village_result):
    global act

    act = 2
    
    # Update Discord Status
    update_presence(
        state="Playing Campaign",
        details="Chapter 1 - Act 2",
        large_image="corrupted_shadows",
        large_text="Corrupted Shadows",
        small_image="corrupted_book",
        small_text=f"{player.name} | HP: {player.hp}/{player.max_hp} | Lvl: {player.level} | Chapter 1 - Act 2"
    )
    # Encounter 1
    corrupted_orc = CorruptedOrc(5)
    corrupted_goblin_1 = CorruptedGoblin(2)
    corrupted_goblin_2 = CorruptedGoblin(3,True)
    corrupted_goblin_3 = CorruptedGoblin(2)

    clear_screen()
    animate_title(Fore.GREEN + "Act II - The Forest")
    print("")
    time.sleep(3)
    clear_screen()

    if village_result == "fight":
        typewriter(Fore.WHITE + "As you walk through the forest, a strange sense of dread settles in...")
        typewriter("Something about this place feels very, very wrong.")
        print("")
        time.sleep(2)
        typewriter("You hear laughter — the kind you'd expect from goblins lying in wait.")
        typewriter("But the sound is colder, darker. As if even the goblins aren't quite themselves.")
        time.sleep(1)
        print("")
        typewriter("Eventually, you find yourself in a clearing... Feeling safe, you lower your guard.")
        print("")
        time.sleep(1)
        typewriter("But as you're about to sit down for a quick rest, three goblins jump from the bushes-- daggers")
        typewriter("in hand, ready for vengeance. Their eyes glow an unnatural color, confirming your suspicion that")
        typewriter("something isn't quite right.")
        print("")
        time.sleep(1)
        typewriter("The goblins surround you, but show no interest in your coin. The clearing grows quiet, all you can")
        typewriter("hear is the cold laughter of the goblins closing in on you... You've got to do something!")
        print("")
        time.sleep(2)

        # Battle
        enemies = [corrupted_goblin_1, corrupted_goblin_2, corrupted_goblin_3]
        battle(player, enemies, battle_mode="multi")
        update_presence("Playing Campagin", "Chapter 1 Act 2")

        # After Battle
        typewriter(Fore.WHITE + "The three goblins lay defeated on the ground. While two are laying lifeless, one")
        typewriter("is still twitching violently. You can hear its screams of pain...You")
        typewriter("think— that poor thing.")
        print("")
        time.sleep(1)
        typewriter(Fore.WHITE + "After a well-deserved rest, you leave the clearing, pushing yourself through")
        typewriter("the dense forest.")
        print("")
        time.sleep(2)
        heal_player_precent(player, 30) 
        typewriter(Fore.WHITE+"As you contiune through the forest, the fog around you grows thick, the sense of dread from before returns, but")
        typewriter("worse than before...")
        print("")
        time.sleep(1)
        typewriter("As your about to lose hope, you see it: The flickering light from a torch or fire, The feeling of warmth draws you")
        typewriter("towards it, almost like you're in a trance")
        print("")
        time.sleep(1)
        typewriter("You arrive at the source of the light — the Goblin Camp. You hear the wicked laughter of the goblins. They don't sound")
        typewriter('cold or dark, but that only makes it worse')
        print("")
        return

    elif village_result == "flee":
        typewriter(Fore.WHITE + "As you rush through the forest, you lose your sense of direction.")
        typewriter("but maybe that wasn't the best idea, as you find yourself")
        typewriter("face to face with an " + Fore.RED + "Orc." + Fore.WHITE)
        print("")
        time.sleep(2)
        typewriter(Fore.WHITE + "Only... something seems wrong. The Orc's eyes glow a bright" + Fore.MAGENTA + "purple")
        typewriter("color" + Fore.WHITE + " and its behavior seems unnatural, almost like it's acting without will.")
        time.sleep(1)
        typewriter(Fore.BLUE + "Before you know it, the Orc is on top of you, ready to smash you into itty, bitty, pieces!")
        print(Fore.RESET + "")
        print("")

        # Battle with Orc
        battle(player, corrupted_orc, battle_mode="single", bonus_ap=2)
        update_presence("Playing Campagin", "Chapter 1 Act 2")

        # After Battle
        typewriter(Fore.WHITE + "The Orc seems to be knocked out— for now... You search it for anything of value and find")
        typewriter("3 Health Potions")
        print("")
        health_potion_1 = create_item("Health Potion")
        health_potion_2 = create_item("Health Potion")
        health_potion_3 = create_item("Health Potion")
        player.inventory.add_item(health_potion_3)
        player.inventory.add_item(health_potion_1)
        player.inventory.add_item(health_potion_2)
        print(Fore.GREEN+player.name+" found 3 Health Potions")
        print("")
        time.sleep(2)
        typewriter(Fore.WHITE+"Afterwards, you hear the Orc grunt. Better leave before he wakes up!")
        print("")
        time.sleep(2)
        typewriter(Fore.WHITE+"You leave the Orc, and head deeper into the forest, the fog grows thick, and you seem to")
        typewriter("have lost your way...")
        print("")
        time.sleep(2)
        typewriter("Eventaully, you hear a wicked laughter. As the fog clears you find yourself at a Camp full")
        typewriter("goblins, and they don't look very nice!")
        print("")
        return

def goblin_camp(player):
    global act
    act = 3
    # Update Discord Status
    update_presence(
        state="Playing Campaign",
        details="Chapter 1 - Act 3",
        large_image="corrupted_shadows",
        large_text="Corrupted Shadows",
        small_image="corrupted_book",
        small_text=f"{player.name} | HP: {player.hp}/{player.max_hp} | Lvl: {player.level} | Chapter 1 - Act 3"
    )
    ap_bonus = 0
    # Regular Goblin Encounter Objects
    goblin_1 = Goblin(3)
    goblin_2 = Goblin(3)
    goblin_3 = Goblin(2)
    goblin_4 = Goblin(3)
    main_corrupted_goblin = CorruptedGoblin(5)

    typewriter(Fore.WHITE+"You hide behind a nearby tree, scouting out the nearby camp, You spot 5 goblins in")
    typewriter("camp, but one seems to be acting strange. instead of laughing it's grumbling, almost like it's")
    typewriter("under someone or something's influence. You take a moment to think about your next move")
    print("")
    time.sleep(3)
    # Pre-corruption Encounter
    enemies = [goblin_1,goblin_2,goblin_3,goblin_4,main_corrupted_goblin]
    print(Fore.YELLOW + "What will you do?".center(50))
    print(Fore.CYAN + "=" * 50)
    print(Fore.GREEN + " [1] ".ljust(6) + "Fight the Goblins")
    print(Fore.GREEN + " [2] ".ljust(6) + "Observe the Goblins")
    print(Fore.GREEN + " [3] ".ljust(6) + "Sneak to leave quietly")
    print(Fore.YELLOW + " [4] ".ljust(6) + "Check Inventory")
    print(Fore.CYAN + "=" * 50)

    while True:
        choice = input(Fore.YELLOW + "> ").strip()

        if choice == "1":
            typewriter(Fore.WHITE+"You summon all of the courge you have left and charge head first into")
            typewriter("the camp. The goblin that was acting strange snaps back into realitiy and all five")
            typewriter("ready themselves for your assault!")
            print("")
            time.sleep(2)
            battle(player,enemies,battle_mode="multi",bonus_ap=ap_bonus)
            update_presence("Playing Campagin", "Chapter 1 Act 3")
        elif choice == "2":
            chance = random.randint(1,2)
            typewriter(Fore.YELLOW+"You attempt to observe the Goblins behavior")
            print("")
            if ap_bonus == 0:
                if chance == 1:
                    typewriter(Fore.WHITE+"You crouch low behind the trees, using them as cover. You observe")
                    typewriter("the goblins and notice one is snapping in and out of reality, and one")
                    typewriter("appears to have a hurt leg. Maybe you can use this to your advantage")
                    print("")
                    time.sleep(3)
                    typewriter("Your keen observation gives you a slight advantage")
                    print("")
                    time.sleep(1)
                    print(Fore.YELLOW + "What will you do?".center(50))
                    print(Fore.CYAN + "=" * 50)
                    print(Fore.GREEN + " [1] ".ljust(6) + "Fight the Goblins")
                    print(Fore.GREEN + " [2] ".ljust(6) + "Observe the Goblins")
                    print(Fore.GREEN + " [3] ".ljust(6) + "Sneak to leave quietly")
                    print(Fore.YELLOW + " [4] ".ljust(6) + "Check Inventory")
                    print(Fore.CYAN + "=" * 50)
                    ap_bonus += 1
                else:
                    typewriter(Fore.RED+"You attempt to observe from behind the trees, but the tension is too high.")
                    typewriter("one of them notice your slight movements and blows a strange flute. You hear the sound")
                    typewriter("of the goblins closing in, ready to pounce!")
                    print("")
                    battle(player,enemies,battle_mode="multi",bonus_ap=ap_bonus)
                    update_presence("Playing Campagin", "Chapter 1 Act 3")
                    break
            else:
                print(Fore.RED+"You've already observed and can't observe again!")
                print("")
        elif choice == "3":
            typewriter(Fore.RED+"You attempt to sneak by the camp, but accidently step on a")
            typewriter("twig. The sound echoes through the forest, and the goblins notice")
            typewriter('your flee attempt!')
            print("")
            battle(player,enemies,battle_mode="multi",bonus_ap=ap_bonus)
            update_presence("Playing Campagin", "Chapter 1 Act 3")
            break
        elif choice == "4":
            player.inventory.use_non_combat_item(player)
            time.sleep(1)
            print(Fore.YELLOW + "What will you do?".center(50))
            print(Fore.CYAN + "=" * 50)
            print(Fore.GREEN + " [1] ".ljust(6) + "Fight the Goblins")
            print(Fore.GREEN + " [2] ".ljust(6) + "Observe the Goblins")
            print(Fore.GREEN + " [3] ".ljust(6) + "Sneak to leave quietly")
            print(Fore.YELLOW + " [4] ".ljust(6) + "Check Inventory")
            print(Fore.CYAN + "=" * 50)
    
    typewriter(Fore.WHITE+"You find yourself in the middle of the camp, all of the goblins lying")
    typewriter("on the ground, defeated. Except one...")
    print("")
    time.sleep(1)
    typewriter(Fore.WHITE + "You recognize this Goblin, it was the one acting strange when you first")
    typewriter(Fore.WHITE + "entered the camp. But something seems even more off than before. The")
    typewriter(Fore.MAGENTA + "Goblin's eyes glow purple, and the sky grows dark. The Goblin taps each")
    typewriter(Fore.MAGENTA + "of the defeated Goblins, and one by one they begin to rise. But this time")
    typewriter(Fore.MAGENTA + "their eyes glow purple, mirroring their leader")
    print("")
    return ap_bonus
    

def timed_encounter(player, ap_bonus):
    turn_count = 0
    max_turns = 5
    win_count = 0
    fought_single_goblin = False

    corrupted_goblin_1 = CorruptedGoblin(3)
    corrupted_goblin_2 = CorruptedGoblin(5)
    corrupted_goblin_3 = CorruptedGoblin(5)
    corrupted_goblin_4 = CorruptedGoblin(5)
    corrupted_goblin_5 = CorruptedGoblin(7)

    enemies = [corrupted_goblin_1, corrupted_goblin_2, corrupted_goblin_3, corrupted_goblin_4, corrupted_goblin_5]

    def calculate_flee_chance(player):
        base_chance = 10
        kill_bonus = 10 * win_count
        speed_bonus = min(player.speed // 10, 3) * 10
        
        total_chance = base_chance + kill_bonus + speed_bonus
        total_chance = min(total_chance, 100)
        
        return total_chance

    while turn_count < max_turns and win_count < 5:
        turns_left = max_turns - turn_count

        print(Fore.RED + Style.BRIGHT + "TIME IS RUNNING OUT!".center(50))
        print(Fore.RED + "=" * 50)

        if turns_left <= 2:
            print(Fore.RED + "Turns Remaining: ".center(25) + str(turns_left).center(25))
        else:
            print(Fore.YELLOW + "Turns Remaining: ".center(25) + str(turns_left).center(25))

        print(Fore.RED + "=" * 50)

        flee_chance = calculate_flee_chance(player)

        print(Fore.LIGHTRED_EX + " [1] " + "Attack all Goblins! (5 Turns)" if not fought_single_goblin else " [1] " + "You have already fought a single Goblin.")
        print(Fore.LIGHTRED_EX + " [2] " + "Attack a single Goblin (2 Turns) ")
        print(Fore.LIGHTRED_EX + " [3] Flee: " + str(flee_chance) + "% (1 Turn) ")
        print(Fore.LIGHTRED_EX + " [4] " + "Steal From the Goblins (1 Turn) ")
        print(Fore.LIGHTRED_EX + " [5] " + "Check Inventory (1 Turn) ")
        print(Fore.RED + "=" * 50)
        
        print(Style.RESET_ALL, end="")

        choice = input("> ").strip()

        if choice == "1" and not fought_single_goblin:
            turn_count += 5
            typewriter("You ignore the Goblins' strange new form and charge at them with full force. The")
            typewriter("Goblins don't react until the Leader blows their whistle, giving you an advantage! ")
            print("")
            if ap_bonus > 0:
                typewriter(Fore.GREEN + "Your observations from before come in handy, giving you more of an")
                typewriter("advantage against the goblins! ")
                print("")
            battle_ap_bonus = ap_bonus + 2
            battle(player, enemies, "multi", battle_ap_bonus)
            update_presence("Playing Campagin", "Chapter 1 Act 3")
            typewriter(Fore.GREEN + "You defeated all the Goblins and the camp lays dormant." + Fore.WHITE + " You inspect the")
            typewriter("leader goblin and find the flute the Goblin was blowing.")
            print("")
            cleansing_flute = create_item("Cleansing Flute")
            player.inventory.add_item(cleansing_flute)
            print(Fore.WHITE + player.name + " obtained the Cleansing Flute")
            print("")
            time.sleep(1)
            typewriter("You walk out of the camp, the exit to the forest is just up ahead. The dark sky brightens")
            typewriter("and the sight of freedom keeps you going. You sigh a sigh of relief. The danger is behind")
            typewriter("you-- For now... ")
            print("")
            time.sleep(2)
            return "victory"

        elif choice == "2":
            turn_count += 2 
            goblin_to_fight = random.choice(enemies)

            typewriter(Fore.WHITE + "You challenge a single Goblin to fight. The leader laughs, and")
            typewriter("points at you, the Goblin charges forward with his dagger, ready to fight!")
            print("")

            battle(player, [goblin_to_fight], "single", ap_bonus)
            update_presence("Playing Campagin", "Chapter 1 Act 3")
            
            win_count += 1
            fought_single_goblin = True
            typewriter(Fore.WHITE + "You have defeated", Fore.GREEN + str(win_count) + "/" + Fore.WHITE + "5" + Fore.WHITE + " Goblins")
            print("")
        
        elif choice == "3":
            turn_count += 1
            typewriter(Fore.BLUE+"You attempt to flee from the camp, The leader blows his whistle, and the")
            typewriter("Goblins start chasing")
            if random.randint(1, 100) <= flee_chance:
                typewriter(Fore.WHITE+"You manage to outrun the approaching Goblins, your heart pounding")
                typewriter("a thousand times over. The sounds of their footsteps and the leader's whistle")
                typewriter("fade behind you, and you breathe a sigh of relief. The exit is just up ahead")
                print("")
                return "victory"
            else:
                typewriter(Fore.RED+"You fail to escape, the goblins close in, daggers in hand, Ready to stab you")
                typewriter("into little pieces")
                print("")
                continue
        elif choice == "4":
            turn_count += 1
            typewriter(Fore.YELLOW + "You attempt to sneak past the goblins and steal something of value...")
            print("")

            fail_roll = random.randint(1, 100)

            if fail_roll <= 30:
                typewriter(Fore.RED + "You fail to steal anything and get noticed by the goblins. You lose your chance!")
                print("")
            else:
                steal_roll = random.randint(1, 100)

                if steal_roll <= 60:
                    stolen_item = random.choice(["Goblin Tooth", "Health Potion", "Goblin Dagger"])
                    if stolen_item == "Goblin Tooth":
                        typewriter(Fore.GREEN + "You successfully steal a Goblin Tooth!")
                        print("")
                        tooth = create_item("Goblin Tooth")
                        player.inventory.add_item(tooth)
                    elif stolen_item == "Health Potion":
                        typewriter(Fore.GREEN + "You successfully steal a Health Potion!")
                        print("")
                        potion = create_item("Health Potion")
                        player.inventory.add_item(potion)
                    elif stolen_item == "Goblin Dagger":
                        typewriter(Fore.GREEN + "You successfully steal a Goblin Dagger!")
                        print("")
                        dagger = create_item("Goblin Dagger")
                        player.inventory.add_item(dagger)
                elif steal_roll <= 85:
                    typewriter(Fore.GREEN + "You successfully steal 3 Health Potions!")
                    print("")
                    potion_x3 = create_item("Health Potion x3")
                    player.inventory.add_item(potion_x3)
                else:
                    money_amount = random.randint(100, 1000)
                    typewriter(Fore.GREEN + "You successfully steal " + str(money_amount) + " coins!")
                    print("")
                    player.money += money_amount


        if turn_count >= max_turns:
            typewriter(Fore.RED + Style.BRIGHT + "You ran out of time, the Goblins surround you, daggers in")
            typewriter("hand. They all circle you and stab you.")
            if player.hp > 75:
                typewriter("The goblins viciously stab you, but eventually grow bored. The leader blows his flute")
                typewriter("and the Goblins lay off, allowing you to barely escape.")
                print(Fore.RESET + "")
                player.hp -= 75
                return "fail"
            else:
                death_screen()

def ending(player, encounter_result):
    # Update Discord Status
    update_presence(
        state="Playing Campaign",
        details="Chapter 1 - Ending",
        large_image="corrupted_shadows",
        large_text="Corrupted Shadows",
        small_image="corrupted_book",
        small_text=f"{player.name} | HP: {player.hp}/{player.max_hp} | Lvl: {player.level} | Chapter 1 - Ending"
    )
    if encounter_result == "fail":
        typewriter(Fore.WHITE + "You limp towards the exit and make it out of the forest. But")
        typewriter("as you think you're in the clear, you reach the Iron Fist, but only... it's")
        typewriter("burning. All you can hear is groaning from the inside...")
        print("")
        # End of Chapter 1
        # Move to Chapter 2 - From the Shadows
        return
    if encounter_result == "victory":
        typewriter(Fore.WHITE + "You exit the forest, but find yourself at the Iron Fist, and it looks")
        typewriter("like the monsters have already gotten there. The entire place is burning, and all")
        typewriter("you can hear are groaning and grumbling from inside.")
        print("")
        # End of Chapter 1
        # Move to Chapter 2 - From the Shadows
        return
    else:
        print(Fore.RED + "An error has occurred. Please report this!")
        return "error"