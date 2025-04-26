from player import Player
from colorama import Fore, Style
import random
import os
from screens import show_character_sheet
from text_utils import clear_screen, typewriter, animate_title, dice_roll_animation
from game_data import difficulty

def character_creation():
    global difficulty
    clear_screen()
    animate_title(Fore.MAGENTA + "Character Creation", delay=0.07)
    print("\n")

    # Asking for the character name
    typewriter(Fore.YELLOW + "What is your name?", delay=0.03)
    name = input(Fore.CYAN + "> ")
    while name.strip() == '':
        typewriter(Fore.RED + "You must enter a name!", delay=0.03)
        name = input(Fore.CYAN + "> ")
        
    print("\n")
    
    # Difficulty selection
    typewriter(Fore.YELLOW + "Select difficulty (1-100)", delay=0.03)
    difficulty_input = input(Fore.CYAN + "> ")
    while not difficulty_input.isdigit() or not (1 <= int(difficulty_input) <= 100):

        typewriter(Fore.RED + "Invalid input! Please choose a number between 1 and 100.", delay=0.03)
        difficulty_input = input(Fore.CYAN + "> ")

    difficulty = int(difficulty_input)

    # Difficulty-based color and warning
    if difficulty <= 25:
        difficulty_color = Fore.GREEN
        warning_message = Fore.YELLOW + "\nWarning: Enemies will be significantly weaker. Consider increasing difficulty for more of a challenge.\n"
    elif difficulty <= 50:
        difficulty_color = Fore.YELLOW
        warning_message = ""
    else:
        difficulty_color = Fore.RED
        warning_message = Fore.YELLOW + "\nWarning: Enemies will be significantly stronger and very punishing. Consider lowering difficulty if you're new.\n"

    print(difficulty_color + "\nSelected Difficulty: " + str(difficulty) + Style.RESET_ALL)
    
    # Show the warning if necessary
    if warning_message:
        typewriter(warning_message, delay=0.03)

    print("\n")
    
    # Roll stats
    typewriter(Fore.MAGENTA + "Rolling your stats...", delay=0.04)
    print()

    hp = random.choice(range(50, 151, 5))
    strength = random.randint(5, 15)
    speed = random.randint(0, 15)
    intelligence = random.randint(50, 200)
    defense = 0
    money = 1000

    # Show dice rolls with animation
    dice_roll_animation("HP", hp)
    dice_roll_animation("Strength", strength)
    dice_roll_animation("Speed", speed)
    dice_roll_animation("Intelligence", intelligence)

    print("\n")
    print(Fore.CYAN + "Character Creation Complete!" + Style.RESET_ALL)

    print("\n")

    player = Player(name, hp, strength, speed, intelligence, defense, money,None)
    show_character_sheet(player)

    return player
