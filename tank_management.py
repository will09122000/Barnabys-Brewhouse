"""
This module is reponsible for fetching the status of each tank.
"""
import json
from logs import log_warning

def get_tank_status() -> dict:
    """
    This function reads the tank json file, saves and returns its
    contents to a dictionary.
    """
    with open('tanks.json', 'r') as tanks_file:
        try:
            tank_status = json.load(tanks_file)
        except ValueError as warning:
            tank_status = []
            log_warning(warning)
    return tank_status