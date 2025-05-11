from player import Player
from colorama import Fore, Style
import random
import os
import time
from screens import show_character_sheet
from text_utils import clear_screen, typewriter, animate_title, dice_roll_animation
from tower.tower_data import tower_difficulty
from discord import update_presence

def create_tower_run():
    # Update the presence to show tower creation
    update_presence("Ascending the Tower", "Creating a Tower Avatar")
    clear_screen()
    animate_title(Fore.MAGENTA + "Tower Creation", delay=0.07)
    print("\n")

    # Character Name Input
    typewriter(Fore.YELLOW + "What is your name, adventurer?", delay=0.03)
    name = input(Fore.CYAN + "> ")
    while name.strip() == '':
        typewriter(Fore.RED + "You must enter a name! Your identity awaits!", delay=0.03)
        name = input(Fore.CYAN + "> ")
        
    print("\n")

    # Difficulty Selection
    typewriter(Fore.YELLOW + "Select your Tower difficulty", delay=0.03)
    print("")
    print(Fore.GREEN + "Easy - Enemies are weak for a first playthrough.")
    print(Fore.YELLOW + "Normal - Balanced enemies for a regular playthrough.")
    print(Fore.RED + "Hard - Tanky enemies for a challenging playthrough.")
    print(Fore.MAGENTA + "Hardcore - Extreme danger, dying is permanent!")
    print("")
    difficulty_input = input(Fore.CYAN + "> ").lower()

    while difficulty_input not in ['easy', 'normal', 'hard', 'hardcore']:
        typewriter(Fore.RED + "Invalid selection. Please choose a valid difficulty.", delay=0.03)
        print("")
        difficulty_input = input(Fore.CYAN + "> ").lower()

    # Setting Difficulty and Warnings
    if difficulty_input == "easy":
        tower_difficulty = "easy"
    elif difficulty_input == "normal":
        tower_difficulty = "normal"
    elif difficulty_input == "hard":
        tower_difficulty = "hard"
        typewriter(Fore.RED + "Warning: Hard difficulty is NOT recommended for a first playthrough!", delay=0.03)
        print("")
    elif difficulty_input == "hardcore":
        tower_difficulty = "hardcore"
        typewriter(Fore.MAGENTA + "Warning: Hardcore difficulty is brutally punishing. Proceed with caution!", delay=0.03)
        print("")

    # Confirmation of Difficulty
    typewriter(Fore.YELLOW + "Tower difficulty set to " + tower_difficulty.capitalize() + ".", delay=0.03)
    time.sleep(1)

    # Tower Avatar Creation
    typewriter(Fore.YELLOW + "Creating your Tower Avatar...", delay=0.03)
    print("")

    # Stats Rolling
    typewriter(Fore.MAGENTA + "Rolling your stats...\n", delay=0.04)

    hp = random.choice(range(100, 251, 5))
    strength = random.randint(10, 25)
    speed = random.randint(0, 15)
    intelligence = random.randint(50, 200)
    defense = 0
    money = 0

    dice_roll_animation("HP", hp)
    dice_roll_animation("Strength", strength)
    dice_roll_animation("Speed", speed)
    dice_roll_animation("Intelligence", intelligence)

    # Summary of Avatar Creation
    print("\n")
    typewriter(Fore.CYAN + "Tower Avatar Creation Complete!", delay=0.03)
    print("\n")

    # Create Player
    player = Player(name, hp, strength, speed, intelligence, defense, money, None)
    show_character_sheet(player)
    clear_screen()

    # Final Message
    typewriter(Fore.YELLOW + "You are now ready to face the Tower!\n", delay=0.03)
    update_presence(
        state="Ascending the Tower",
        details="Preparing for the Challenge",
        large_image="corrupted_shadows",
    )
    time.sleep(3)

    return player, True
