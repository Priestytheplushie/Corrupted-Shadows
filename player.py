class Player:
    def __init__(self, name, hp, strength, speed, intelligence, defense, money):
        self.name = name
        self.hp = hp
        self.strength = strength
        self.speed = speed
        self.intelligence = intelligence
        self.defense = defense
        self.money = money
        self.max_hp = self.hp
        self.status_effects = []