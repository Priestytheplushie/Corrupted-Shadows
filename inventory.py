from colorama import Fore, Style
from items import Item,Weapon,Potion
from item_data import *

class Inventory:
    def __init__(self):
        self.items = []

    def add_item(self,item):
        self.items.append(item)

    def show_inventory(self):
        if not self.items:
            print(Fore.RED + "Your inventory is empty!")
            print('')
            return
        print(Fore.YELLOW + "Inventory:" + Style.RESET_ALL)
        for index, item in enumerate(self.items):
            print(Fore.GREEN + str(index + 1) + ". " + item.name + Style.RESET_ALL)
            print("   Description: " + item.description)
            if isinstance(item, Weapon) and item.durability is not None:
                print("   Durability: " + str(item.durability))
                print("")

    def use_item(self, player, index, targets=None):
        if index < 0 or index >= len(self.items):
            print(Fore.RED + "Invalid item selection! (Does it Exist?)")
            print("")
            return

        item = self.items[index]
        
        if isinstance(item, Weapon):
            print(Fore.YELLOW + player.name + " uses " + item.name + "!" + Style.RESET_ALL)
            print("")
            item.equip(player)

        elif isinstance(item, Potion):
            print(Fore.YELLOW + player.name + " uses " + item.name + "!" + Style.RESET_ALL)
            item.use(player)

        elif isinstance(item, CleansingFlute):
            print(Fore.YELLOW + player.name + " plays the " + Fore.GREEN + item.name + Fore.WHITE + "!" + Style.RESET_ALL)
            print("")
            
            if targets:  
                if not isinstance(targets, list):
                    targets = [targets] 
                item.use(player, targets)  
            else:
                print(Fore.RED + "No target to cleanse!" + Style.RESET_ALL)
        elif isinstance(item, UseableItem):
            print(Fore.YELLOW + player.name + " uses the " + Fore.GREEN + item.name + Fore.WHITE + "!" + Style.RESET_ALL)
            print("")
            
            if targets:  
                if not isinstance(targets, list):
                    targets = [targets] 
                item.use(player, targets)  
            else:
                print(Fore.RED + "No target to use on!" + Style.RESET_ALL)

        if isinstance(item, Weapon) and item.durability == 0:
            self.items.remove(item)
        elif isinstance(item, Potion) and item.quantity == 0:
            self.items.remove(item)
        elif isinstance(item, CleansingFlute) and item.durability == 0:
            self.items.remove(item)
        elif isinstance(item, UseableItem) and item.durability == 0:
            self.items.remove(item)

    def use_non_combat_item(self, player):
        print(Fore.YELLOW + "--- Inventory ---")
        print(Fore.CYAN + "-" * 40)

        if player.weapon:
            weapon_text = Fore.GREEN + "Weapon Equipped: " + player.weapon.name
            if hasattr(player.weapon, "durability") and hasattr(player.weapon, "max_durability"):
                weapon_text += " | Durability: " + str(player.weapon.durability) + "/" + str(player.weapon.max_durability)
            print(weapon_text)
        else:
            print(Fore.RED + "No weapon equipped.")

        if player.inventory.items:
            print(Fore.YELLOW + "Items in your inventory:")
            for i, item in enumerate(player.inventory.items):
                item_text = Fore.GREEN + str(i + 1) + ". " + item.name + " - " + item.description
                if hasattr(item, "durability") and hasattr(item, "max_durability"):
                    item_text += " | Durability: " + str(item.durability) + "/" + str(item.max_durability)
                print(item_text)
        else:
            print(Fore.RED + "Your inventory is empty.")

        print(Fore.CYAN + "-" * 40)
        print("b. Back")
        print("1. Use Item")
        print("2. Equip Weapon")
        print("3. Unequip Weapon")

        while True:
            choice = input(Fore.YELLOW + "> ").strip().lower()

            if choice == "b":
                break

            if choice == "1":
                if player.inventory.items:
                    print(Fore.YELLOW + "Choose an item by number to use (or b to go back):")
                    for i, item in enumerate(player.inventory.items):
                        item_text = Fore.GREEN + str(i + 1) + ". " + item.name + " - " + item.description
                    if hasattr(item, "durability") and hasattr(item, "max_durability"):
                        item_text += " | Durability: " + str(item.durability) + "/" + str(item.max_durability)
                    elif hasattr(item,"quantity"):
                        item_text += " | Quantity: " + str(item.quantity)
                    print(item_text)
                    while True:
                        item_choice = input(Fore.YELLOW + "> ").strip().lower()
                        if item_choice == 'b':
                            break
                        try:
                            item_choice = int(item_choice) - 1
                            if 0 <= item_choice < len(player.inventory.items):
                                item = player.inventory.items[item_choice]
                                if isinstance(item, Potion):
                                    item.use(player)
                                    print(Fore.GREEN + item.name + " used successfully!")
                                    player.inventory.items.remove(item)
                                else:
                                    print(Fore.RED + "This item cannot be used here.")
                                break
                            else:
                                print(Fore.RED + "Invalid index. Try again.")
                        except ValueError:
                            print(Fore.RED + "Please enter a valid number.")
                else:
                    print(Fore.RED + "Your inventory is empty.")
                continue

            elif choice == "2":
                if player.weapon:
                    print(Fore.YELLOW + "You already have a weapon equipped: " + player.weapon.name)
                else:
                    print(Fore.YELLOW + "Choose a weapon to equip (or b to go back):")
                    available_weapons = [item for item in player.inventory.items if isinstance(item, Weapon)]
                    if available_weapons:
                        for i, weapon in enumerate(available_weapons):
                            weapon_text = Fore.GREEN + str(i + 1) + ". " + weapon.name + " - " + weapon.description
                            if hasattr(weapon, "durability") and hasattr(weapon, "max_durability"):
                                weapon_text += " | Durability: " + str(weapon.durability) + "/" + str(weapon.max_durability)
                            print(weapon_text)
                        while True:
                            weapon_choice = input(Fore.YELLOW + "> ").strip().lower()
                            if weapon_choice == 'b':
                                break
                            try:
                                weapon_choice = int(weapon_choice) - 1
                                if 0 <= weapon_choice < len(available_weapons):
                                    player.equip_weapon(available_weapons[weapon_choice])
                                    print(Fore.GREEN + "Equipped " + player.weapon.name)
                                    break
                                else:
                                    print(Fore.RED + "Invalid index. Try again.")
                            except ValueError:
                                print(Fore.RED + "Please enter a valid number.")
                    else:
                        print(Fore.RED + "No weapons available in your inventory.")
                continue

            elif choice == "3":
                if player.weapon:
                    print(Fore.YELLOW + "Unequipping your weapon: " + player.weapon.name)
                    player.unequip_weapon()
                    print(Fore.GREEN + "Weapon unequipped.")
                else:
                    print(Fore.RED + "No weapon equipped.")
                continue

            else:
                print(Fore.RED + "Invalid option. Try again.")