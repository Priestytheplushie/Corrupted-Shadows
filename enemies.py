from colorama import Fore, Style
import random
import math

class Enemy:
    def __init__(self,name,hp,strength,speed,intelligence,defense):
        self.name = name
        self.hp = hp
        self.strength = strength
        self.speed = speed
        self.intelligence = intelligence
        self.defense = defense
        self.max_hp = self.hp
        self.status_effects = []

    def basic_attack(self,target):
        target.hp -= self.strength
        target.hp = max(target.hp, 0)
        print(Fore.WHITE+self.name,Fore.RED+"delt",self.strength,"damage!")
        print("")

class Goblin(Enemy):
    def __init__(self,level):
        self.name = "Goblin"
        self.hp = 75 + level
        self.strength = 5 + level
        self.speed = 10
        self.intelligence = 0
        self.defense = level
        self.max_hp = self.hp
    def rob(self,target):
        if target.money <= 0:
            print(Fore.WHITE+self.name,"attempted to rob you but")
            print("you had no coins to steal!")
            print("")
        else:
            target.hp -= self.strength
            target.hp = max(target.hp, 0)
            steal = random.randint(1,target.money)
            target.money -= steal
            print(self.name,Fore.RED+"stole",Fore.YELLOW+"$"+str(steal),Fore.RED+"and delt",self.strength,"damage!")
            print("")