"""
This module handles fetching the inventory from the json file
and updating the inventory when a manual update is requested.
"""
import json
from flask import request
from logs import log_warning, log_info

def get_inventory() -> dict:
    """
    This function reads the tank json file and saves its contents to
    a dictionary.
    """
    with open('inventory.json', 'r') as inventory_file:
        try:
            inventory = json.load(inventory_file)
        except ValueError as warning:
            inventory = []
            log_warning(warning)
    return inventory

def update_inventory() -> None:
    """
    This function overwrites the current inventory of a beer type
    with the value and beer type provided by the user via the
    user interface using request.
    """
    beer_type = request.args.get('beer_type')
    new_quantity = int(request.args.get('new_quantity'))
    inventory = get_inventory()
    for beer in inventory:
        if beer['beer_type'] == beer_type:
            beer['quantity'] = new_quantity
    with open('inventory.json', 'w') as inventory_file:
        json.dump(inventory, inventory_file, indent=2)

    log_info(beer_type + ' Stock has been updated to: ' + \
             str(new_quantity))
