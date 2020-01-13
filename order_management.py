"""
This module is responsible for handling customer orders inputted by the
user via the user interface.
"""

import time
import datetime
import json
from flask import request
from inventory import get_inventory
from logs import log_warning, log_info

def order_bottles() -> None:
    """
    This function fetches the order details using request and saves
    it as a dictionary. This is then appended to the orders json file.
    """
    order = {
        'timestamp': str(time.strftime('%H:%M:%S')) + ' ' + \
        str(datetime.date.today()),
        'beer_type': request.args.get('beer_type'),
        'quantity': float(request.args.get('quantity')),
        'date_required': request.args.get('date_required'),
    }
    with open('orders.json', 'r') as orders_file:
        try:
            orders = json.load(orders_file)
        except ValueError as warning:
            orders = []
            log_warning(warning)
    orders.append(order)

    with open('orders.json', 'w') as orders_file:
        json.dump(orders, orders_file, indent=2)

    log_info('New Customer Order: ' + str(order))

def get_orders() -> None:
    """
    This function fetches and returns orders from the orders json file.
    """
    with open('orders.json', 'r') as orders_file:
        try:
            orders = json.load(orders_file)
        except:
            orders = {}
    return orders

def dispatch_order() -> None:
    """
    This function dispatches an order when requested by the user and
    adjusts the inventory accordingly. The order is identifed by the
    timestamp it was entered by the user.
    """
    timestamp = request.args.get('timestamp')
    orders = get_orders()
    for order in orders:
        if order['timestamp'] == timestamp:
            inventory = get_inventory()
            for beer in inventory:
                if order['beer_type'] == beer['beer_type'] and \
                order['quantity'] <= beer['quantity']:
                    beer['quantity'] -= order['quantity']
                    with open('inventory.json', 'w') as inventory_file:
                        json.dump(inventory, inventory_file, indent=2)
                    orders.remove(order)
                    with open('orders.json', 'w') as orders_file:
                        json.dump(orders, orders_file, indent=2)
                    break
            log_info('Customer Order Dispatched: ' + str(order))
