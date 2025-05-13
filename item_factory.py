from items import *
from item_data import item_library
from tower.tower_item_data import tower_library

# Initialize an empty gauntlet library
gauntlet_library = {}

def create_item(name):
    # First, check all libraries (gauntlet_library, tower_library, and item_library)
    data = gauntlet_library.get(name) or tower_library.get(name) or item_library.get(name)
    
    if not data:
        print("Item not found:", name)
        return None

    item_type = data["type"]

    if item_type == "weapon":
        return Weapon(name, data["description"], data["damage"], data["durability"])
    elif item_type == "orc_mace":
        return OrcsMace(name, data["description"], data["damage"], data["durability"])
    elif item_type == "potion":
        return Potion(name, data["description"], data["healing_amount"], data["quantity"])
    elif item_type == "cleansing_flute":
        return CleansingFlute(name, data["description"], data["uses"])
    elif item_type == "aoe_weapon":
        return AOEWeapon(name, data["description"], data["damage"], data["durability"])
    elif item_type == "useable_item":
        return UseableItem(name, data["description"], data["uses"])
    elif item_type == "item":
        return Item(name, data["description"])
    else:
        print("Unknown item type:", item_type)
        return None