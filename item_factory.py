from items import *
from item_data import item_library

def create_item(name):
    data = item_library.get(name)
    if not data:
        print("Item not found:", name)
        return None

    item_type = data["type"]
    base_value = data.get("base_value", 0)

    if item_type == "weapon":
        return Weapon(name, data["description"], data["damage"], data["durability"], base_value)
    if item_type == "orc_mace":
        return OrcsMace(name, data["description"], data["damage"], data["durability"], base_value)
    elif item_type == "potion":
        return Potion(name, data["description"], data["healing_amount"], data["quantity"], base_value)
    elif item_type == "cleansing_flute": 
        return CleansingFlute(name, data["description"], data["uses"], base_value)
    elif item_type == "useable_item": 
        return UseableItem(name, data["description"], data["uses"], base_value)
    elif item_type == "item":
        return Item(name, data["description"], base_value)
    else:
        print("Unknown item type:", item_type)
        return None