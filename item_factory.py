from items import Weapon, Potion, Item
from item_data import item_library

def create_item(name):
    data = item_library.get(name)
    if not data:
        print("Item not found:", name)
        return None

    item_type = data["type"]

    if item_type == "weapon":
        return Weapon(name, data["description"], data["damage"], data["durability"])
    elif item_type == "potion":
        return Potion(name, data["description"], data["healing_amount"], data["quantity"])
    elif item_type == "item":
        return Item(name, data["description"])
    else:
        print("Unknown item type:", item_type)
        return None