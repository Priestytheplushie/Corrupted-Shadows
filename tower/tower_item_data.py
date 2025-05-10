from items import *
from tower.tower_items import *

# Item Types
# item = generic item
# weapon = increases attack 
# potion = restores HP
# ap_potion = grants pernament AP

tower_library = {
    "Iron Sword": {
        "type": "weapon",
        "description": (
            "A sturdy and reliable blade forged from iron\n"
            "Damage: +10"
        ),
        "damage": 10,
        "durability": 25
    },
    "Wooden Sword": {
        "type": "weapon",
        "description": (
            "A crude sword crafted from sturdy wood. Not the flashiest\n"
            "weapon, but it gets the job done.\n"
            "Damage: +5"
        ),
        "damage": 5,
        "durability": 15
    },
    "Goblin Dagger": {
        "type": "weapon",
        "description": (
            "A rigid dagger crafted using a slain Goblin's Tooth"
            "Damage: +7"
        ),
        "damage": 7,
        "durability": 50
    },
    "Obsidian Claymore": {
        "type": "weapon",
        "description": (
            "A heavy claymore crafted from pure obsidian"
            "Damage: +35"
        ),
        "damage": 35,
        "durability": 13
    },
    "Orc's Mace": {
        "type": "orc_mace",
        "description": (
            "A heavy, brutal weapon forged for the fiercest of Orc warriors.\n"
            "Deals devastating AOE damage to all enemies that oppose it\n"
            "Damage: +20"
        ),
        "damage": 20,
        "durability": 20
    },
    "Health Potion": {
        "type": "potion",
        "description": (
            "A simple brew which restores 25 HP"
        ),
        "healing_amount": 25,
        "quantity": 1
    },
    "Potient Health Potion": {
        "type": "potion",
        "description": (
            "A potient brew which restores 50 HP"
        ),
        "healing_amount": 50,
        "quantity": 1
    },
    "Stamina Potion": {
        "type": "ap_potion",
        "description": (
            "A energizing elixir which grants +1 bonus AP pernamently"
        ),
        "ap_amount": 1,
        "quantity": 1
    },
    "Cleansing Flute": {
        "type": "cleansing_flute",
        "description": (
            "A mystical flute carved with ancient runes.\n"
            "Plays a purifying melody that cleanses corrupted foes\n"
            "and soothes the user's soul, reducing their corruption."
        ),
        "uses": 5
    }
}
