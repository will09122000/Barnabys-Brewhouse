"""
This module is responsible for handling the creation, movement and
termination of batches created from the user interface.
"""

import json
import time
import math
import datetime
from flask import request
from logs import log_warning, log_info

def round_down(number: float, decimals=0) -> int:
    """
    https://tinyurl.com/we4ssxc
    """
    multiplier = 10 ** decimals
    return math.floor(number * multiplier) / multiplier

def add_new_batch() -> None:
    """
    This function fetches the batch variables using request and saves
    it as a dictionary. The batches json file is opened, the new batch
    is appended to it and the batches are saved to the same file.
    """
    batch = {
        'timestamp': str(time.strftime('%H:%M:%S')) + ' ' + \
                     str(datetime.date.today()),
        'beer_type': request.args.get('beer_type'),
        'gyle_number': request.args.get('gyle_number'),
        'quantity': float(request.args.get('quantity')),
        'tank_preference': request.args.get('tank_preference'),
        'current_phase': 'Hot Brew in kettle'
    }
    batches = get_batches()
    batches.append(batch.copy())
    with open('batches.json', 'w') as batch_file:
        json.dump(batches, batch_file, indent=2)

    log_info('New Batch: ' + str(batch))

def batch_to_tank(batch: dict) -> bool:
    """
    This function will decide which tank each batch in the batch
    file will be used. It checks if the batch has a tank preference
    which will take priority if so. If no preference was selected the
    next tank that has fermentation and carbonation capability will be
    selected and then if that is not successful the next available tank
    will be chosen. If no tank can be found then 'False' is returned
    and the batch will remain in its current state waiting for a tank
    to become available.
    """
    tank_found = False

    with open('tanks.json', 'r') as tanks_file:
        tanks = json.load(tanks_file)

    for tank in tanks:
        if batch['tank_preference'] != 'None':
            # Batch has a tank preference so this takes priority.
            if batch['tank_preference'] == 'Albert' and \
            tank['name'] == 'Albert' and tank['available']:
                tank['batch'] = batch
                tank['available'] = False
                tank_found = True
            elif batch['tank_preference'] == 'Brigadier' and \
            tank['name'] == 'Brigadier' and tank['available']:
                tank['batch'] = batch
                tank['available'] = False
                tank_found = True
            elif batch['tank_preference'] == 'Camilla' and \
            tank['name'] == 'Camilla' and tank['available']:
                tank['batch'] = batch
                tank['available'] = False
                tank_found = True
            elif batch['tank_preference'] == 'Dylon' and \
            tank['name'] == 'Dylon' and tank['available']:
                tank['batch'] = batch
                tank['available'] = False
                tank_found = True
            elif batch['tank_preference'] == 'Emily' and \
            tank['name'] == 'Emily' and tank['available']:
                tank['batch'] = batch
                tank['available'] = False
                tank_found = True
            elif batch['tank_preference'] == 'Florence' and \
            tank['name'] == 'Florence' and tank['available']:
                tank['batch'] = batch
                tank['available'] = False
                tank_found = True
            # Gertrude and Harry cannot ferment so the tank prference
            # is removed and the batch is re-assigned a tank.
            elif batch['tank_preference'] == 'Gertrude' and \
            tank['name'] == 'Gertrude' and tank['available']:
                batch['tank_preference'] = 'None'
                batch_to_tank(batch)

            elif batch['tank_preference'] == 'Harry' and \
            tank['name'] == 'Harry' and tank['available']:
                batch['tank_preference'] = 'None'
                batch_to_tank(batch)

            elif batch['tank_preference'] == 'R2D2' and \
            tank['name'] == 'R2D2' and tank['available']:
                tank['batch'] = batch
                tank['available'] = False
                tank_found = True
            else:
                batch['tank_preference'] = 'None'
                batch_to_tank(batch)
        else:
            # Finds the next best tank with both fermenting and
            # conditioning capabilities.
            if tank['available'] and tank['fermenter'] and \
            tank['conditioner']:
                tank['batch'] = batch
                tank['available'] = False
                tank_found = True
                break
            if tank['available']:
                tank['batch'] = batch
                tank['available'] = False
                tank_found = True
                break

    with open('tanks.json', 'w') as tanks_file:
        json.dump(tanks, tanks_file, indent=2)
    return tank_found

def next_phase() -> None:
    """
    This function is responsible for changing the phase of a given
    batch when the user clicks the button in the center column. The
    batch is identified via the gyle number. If the batch has finished,
    the inventory is incremented, the batch is removed from the batch
    json file and the tank 'batch' key and the tank is marked as
    available.
    """
    gyle_number = request.args.get('gyle_number')
    BOTTLE_VOLUME = 0.5

    batches = get_batches()
    for batch in batches:
        if batch['gyle_number'] == gyle_number:

            # Hot Brew to Fermentation
            if batch['current_phase'] == \
                'Hot Brew in kettle':
                batch['current_phase'] = 'Fermentation'
                # If a tank cannot be allocated, the current phase is
                # reverted.
                if not batch_to_tank(batch):
                    batch['current_phase'] = 'Hot Brew in kettle'

            # Fermentation to Conditioning and Carbonation
            elif batch['current_phase'] == 'Fermentation':
                batch['current_phase'] = \
                    'Conditioning and Carbonation'
                with open('tanks.json', 'r') as tanks_file:
                    tanks = json.load(tanks_file)
                for tank in tanks:
                    if tank['batch']:
                        if tank['batch']['gyle_number'] == gyle_number:
                            tank['batch']['current_phase'] = \
                            'Conditioning and Carbonation'
                with open('tanks.json', 'w') as tanks_file:
                    json.dump(tanks, tanks_file, indent=2)

            # Conditioning and Carbonation to Bottling
            elif batch['current_phase'] == \
                'Conditioning and Carbonation':
                batch['current_phase'] = \
                    'Bottling and Labelling'
                with open('tanks.json', 'r') as tanks_file:
                    tanks = json.load(tanks_file)
                for tank in tanks:
                    if tank['batch']:
                        if tank['batch']['gyle_number'] == gyle_number:
                            tank['batch'] = {}
                            tank['available'] = True
                with open('tanks.json', 'w') as tanks_file:
                    json.dump(tanks, tanks_file, indent=2)

            # Completing a batch.
            elif batch['current_phase'] == \
                'Bottling and Labelling':
                with open('inventory.json', 'r') as inventory_file:
                    inventory = json.load(inventory_file)
                bottles = round_down(batch['quantity'] * \
                        BOTTLE_VOLUME)
                for bottle in inventory:
                    if bottle['beer_type'] == \
                    batch['beer_type']:
                        bottle['quantity'] += bottles
                with open('inventory.json', 'w') as inventory_file:
                    json.dump(inventory, inventory_file, indent=2)
                batches.remove(batch)
                with open('batches.json', 'w') as batches_file:
                    json.dump(batches, batches_file, indent=2)

            log_info('Batch: ' + str(batch['gyle_number']) + \
                     ' has started a new phase')

        with open('batches.json', 'w') as batch_file:
            json.dump(batches, batch_file, indent=2)

def get_batches() -> dict:
    """Fetches the current batches from the batch json file."""
    with open('batches.json', 'r') as batches_file:
        try:
            batches = json.load(batches_file)
        except ValueError as warning:
            batches = []
            log_warning(warning)
    return batches
