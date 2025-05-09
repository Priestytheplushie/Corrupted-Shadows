from items import *

# Item Types
# item = generic item
# weapon = increases attack 
# potion = restores HP

item_library = {
    "Iron Sword": {
        "type": "weapon",
        "description": (
            "A sturdy and reliable blade forged from iron\n"
            "Damage: +10"
        ),
        "damage": 10,
        "durability": 25,
        "base_value": 100
    },
    "Goblin Dagger": {
        "type": "weapon",
        "description": (
            "A rigid dagger crafted using a slain Goblin's Tooth"
            "Damage: +7"
        ),
        "damage": 7,
        "durability": 35,
        "base_value": 50
    },
    "Goblin Tooth": {
        "type": "item",
        "description": (
            "A small tooth from a goblin. It looks like it's\n"
            "rotting in your hands"
        ),
        "damage": 10,
        "durability": 25,
        "value": 10
    },
    "Orc's Mace": {
        "type": "orc_mace",
        "description": (
            "A heavy, brutal weapon forged for the fiercest of Orc warriors.\n"
            "Deals devastating AOE damage to all enemies that oppose it\n"
            "Damage: +20"
        ),
        "damage": 20,
        "durability": 10,
        "base_value": 200
    },
    "Health Potion": {
        "type": "potion",
        "description": (
            "A simple brew which restores 25 HP"
        ),
        "healing_amount": 25,
        "quantity": 1,
        "value": 25
    },
    "Cleansing Flute": {
        "type": "cleansing_flute",
        "description": (
            "A mystical flute carved with ancient runes.\n"
            "Plays a purifying melody that reverts corrupted creatures\n"
            "back to their natural state."
        ),
        "uses": 5,
        "base_value": 0 # Very rare, should NOT be sold
    },
    "Corrupted Essence": {
        "type": "item",
        "description": (
            "A vile, dark substance that pulses with an eerie energy.\n"
            "It is said to be the essence of corrupted creatures."
        ),
        "value": 0
    },
    "Unstable Shard": {
        "type": "item",
        "description": (
            "A jagged fragment of a mysterious stone that crackles with unstable magic.\n"
            "It seems like it could explode at any moment."
        ),
        "value": 0
    }
}
