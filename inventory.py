from colorama import Fore, Style
from items import Item,Weapon,Potion

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

    def use_item(self, player, index, target=None):
        if index < 0 or index >= len(self.items):
            print(Fore.RED + "Invalid item selection! (Does it Exsist?)")
            print("")
            return
        item = self.items[index]
        if isinstance(item, Weapon):
            print(Fore.YELLOW + player.name + " uses " + item.name + "!" + Style.RESET_ALL)
            print("")
            item.attack(player, target)
        elif isinstance(item, Potion):
            print(Fore.YELLOW + player.name + " uses " + item.name + "!" + Style.RESET_ALL)
            item.use(player)
        if isinstance(item, Weapon) and item.durability == 0:
            self.items.remove(item)
        elif isinstance(item, Potion) and item.quantity == 0:
            self.items.remove(item)