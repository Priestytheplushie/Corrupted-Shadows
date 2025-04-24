from items import *

# Item Types
# item = generic item
# weapon = increases attack 
# potion = restores HP

item_library = {
    "Iron Sword": {
        "type": "weapon",
        "description": "A sturdy blade forged from iron.",
        "damage": 10,
        "durability": 25
    },
    "Health Potion": {
        "type": "potion",
        "description": "Restores 50 HP.",
        "healing_amount": 50,
        "quantity": 1
    },
    "Cleansing Flute": {
        "type": "cleansing_flute",
        "description": "Cleanses monsters from the corruption, reducing their stats",
        "healing_amount": 50,
        "uses": 5
    }
}

