from colorama import Fore, Style
import random
import math
import time
from text_utils import *
from enemies import *
from tower.tower_data import bonus_ap
from items import Item, Weapon

class APPotion(Item):
    global bonus_ap
    def __init__(self, name, description, ap_amount, quantity):
        super().__init__(name, description)
        self.name = name
        self.ap_amount = ap_amount
        self.quantity = quantity

    def use(self, player):
        if self.quantity <= 0:
            print(Fore.RED + self.name + " is out of stock!" + Style.RESET_ALL)
            return
        bonus_ap += self.ap_amount
        self.quantity -= 1
        print(Fore.GREEN + player.name + " uses " + self.name + " and gains " + str(self.ap_amount) + " bonus AP pernamently!" + Style.RESET_ALL)