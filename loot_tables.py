import random
from items import * 
from item_data import item_library 
from item_factory import create_item

loot_tables = {
    "goblin": {
        "Goblin Tooth": 0.30,
        "Health Potion": 0.15
    },
    "orc": {
        "Orc's Mace": 0.05,
        "Health Potion": 0.20
    }
}

corrupted_extras = {
    "generic": {
        "Corrupted Essence": 0.25
    },
    "unstable": {
        "Unstable Shard": 0.10
    }
}


def roll_loot(table_name):
    # If the table name is "none", return an empty list (no loot)
    if table_name == "none" or table_name not in loot_tables:
        return []
    
    loot_drops = []
    table = loot_tables[table_name]
    
    # Iterate over the loot table to determine which items drop
    for item_name, chance in table.items():
        if random.random() <= chance:
            item = create_item(item_name)
            if item:
                loot_drops.append(item)
    return loot_drops

def roll_corrupted_loot(base_table_name, unstable=False):
    if base_table_name == "none":
        return []

    loot = roll_loot(base_table_name)

    for item_name, chance in corrupted_extras["generic"].items():
        if random.random() <= chance:
            item = create_item(item_name)
            if item:
                loot.append(item)

    if unstable:
        for item_name, chance in corrupted_extras["unstable"].items():
            if random.random() <= chance:
                item = create_item(item_name)
                if item:
                    loot.append(item)

    return loot

def roll_corrupted_loot(base_table_name, unstable=False):
    loot = roll_loot(base_table_name)

    for item_name, chance in corrupted_extras["generic"].items():
        if random.random() <= chance:
            item = create_item(item_name)
            if item:
                loot.append(item)

    if unstable:
        for item_name, chance in corrupted_extras["unstable"].items():
            if random.random() <= chance:
                item = create_item(item_name)
                if item:
                    loot.append(item)

    return loot