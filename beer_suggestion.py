"""
This module is responsible for suggesting the type of beer that should
be produced. A score for each beer type is accumulated through the
module and the highest score is the beer that is suggested next.
"""
from inventory import get_inventory
from batch_management import get_batches
from sales_predictions import get_beer_ratio
from logs import log_error

def suggest_beer():
    """
    This function suggests the type of beer that should be produced
    next using the following factors: the current inventory of each
    beer type, the volumes and types of beer in the batches json file
    which includes the state of the tanks and finally the ratio of
    sales for each beer type. Reasons for the choice are generated and
    displayed to the user if relevant.
    """
    scores = {'Red Helles':0, 'Pilsner':0, 'Dunkel':0}

    inventory = get_inventory()
    # Separate score for inventory calculations only to determine the
    # correct reasoning.
    inventory_scores = {'Red Helles':0, 'Pilsner':0, 'Dunkel':0}
    for beer in inventory:
        # Quantity is subtracted as a higher inventory of a beer type
        # should impact it's chances of being suggested negatively.
        scores[beer['beer_type']] -= beer['quantity']
        inventory_scores[beer['beer_type']] += beer['quantity']
    # If all beer types have the same volume then is no point in doing
    # further calculations.
    if all(value == list(inventory_scores.values())[0] \
        for value in inventory_scores.values()):
        inventory_reason = \
        'All type of beer have equal amounts of inventory.'
    else:
        try:
            smallest_inventory = \
            min(inventory_scores, key=inventory_scores.get)

            # Middle value used to calculate the percentage for
            # the reasoning.
            middle_inventory = sum(inventory_scores.values()) - \
            max(inventory_scores.values()) - \
            min(inventory_scores.values())

            inventory_percentage = (1 - \
            min(inventory_scores.values()) / middle_inventory) * 100

            inventory_reason = smallest_inventory + \
            ' has the lowest current inventory by ' + \
            str(round(inventory_percentage)) + '%.'

        except ZeroDivisionError as error:
            log_error(error)
            inventory_reason = ''

    batches = get_batches()
    # Separate score for batch calculations only to determine the
    # correct reasoning.
    batch_scores = {'Red Helles':0, 'Pilsner':0, 'Dunkel':0}
    for batch in batches:
        # Quantity is subtracted as higher batch volumesd of a beer
        # type should impact it's chances of being suggested
        # negatively.
        scores[batch['beer_type']] -= batch['quantity']
        batch_scores[batch['beer_type']] += batch['quantity']
    # If all beer types have the same batch volume then is no point in
    # doing further calculations.
    if all(value == list(batch_scores.values())[0] \
    for value in batch_scores.values()):
        batch_reason = \
        'All type of beer have equal volume currently being processed.'
    else:
        try:
            smallest_batch = min(batch_scores, key=batch_scores.get)

            # Middle value used to calculate the percentage for
            # the reasoning.
            middle_batch = sum(batch_scores.values()) - \
            max(batch_scores.values()) - min(batch_scores.values())

            batch_percentage = (1 - \
            min(batch_scores.values()) / middle_batch) * 100

            batch_reason = \
            smallest_batch + \
            ' has the lowest volume in the tanks and batch queue by ' \
            + str(round(batch_percentage)) + '%.'

        except ZeroDivisionError as error:
            log_error(error)
            batch_reason = ''

    beer_ratio = get_beer_ratio('Barnabys_sales_fabriacted_data.csv')
    if sum(scores.values()) == 0:
        scores = beer_ratio
        ratio_reason = max(scores, key=scores.get) + \
        ' has the largest ratio of sales.'
    else:
        # Favours beer types with a bigger ratio.
        ratio_reason = max(beer_ratio, key=beer_ratio.get) + \
        ' has the largest ratio of sales.'
        scores['Red Helles'] /= beer_ratio['Red Helles']
        scores['Pilsner'] /= beer_ratio['Pilsner']
        scores['Dunkel'] /= beer_ratio['Dunkel']

    return max(scores, key=scores.get), inventory_reason, \
    batch_reason, ratio_reason
