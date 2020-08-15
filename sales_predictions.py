"""
This module is responsible for predicting the demand of each beer type
for a month of sales 3 months from the current date. The average growth
and sales from the same month in the previous years are used to
calculate this prediction.
"""
import datetime
import csv
from math import ceil
import pandas

def growth_rate(data_file: str):
    """
    This function calculates and returns the overall growth rate from
    the csv sales file and the total bottles sold. Each sale is
    separated into the month it is requried, the differnce between the
    total bottles sold for month x and the month before month x is
    divided by the total bottles sold before month x. The growth is
    then the mean of these percentage increases between each month.
    """
    sales_file = pandas.read_csv(data_file)
    sales = sales_file.to_dict()
    dates = []

    for sale in sales['Invoice Number']:
        dates.append(str(sales['Date Required'][sale])[-6:])

    # https://bit.ly/34JJ5I4
    seen = set()
    dates = [x for x in dates if not (x in seen or seen.add(x))]

    # Appends total bottles sold for each month to a dictionary.
    bottles_sold = {}
    for sale in sales['Invoice Number']:
        for month in dates:
            if str(sales['Date Required'][sale])[-6:] == month:
                if month in bottles_sold:
                    bottles_sold[month] += \
                    sales['Quantity ordered'][sale]
                else:
                    bottles_sold[month] = \
                    sales['Quantity ordered'][sale]

    # Converts bottles sold dictionary to a list to be able to
    # calculate the percentage growth.
    percentages = []
    bottles_sold_list = []
    for key, value in bottles_sold.items():
        bottles_sold_list.append(value)
    for sale in range(1, len(bottles_sold_list)):
        percentages.append((bottles_sold_list[sale] - \
        bottles_sold_list[sale-1]) / bottles_sold_list[sale-1])

    # Mean of each month's percentage growth.
    growth = sum(percentages) / len(percentages)
    return growth, bottles_sold

def get_beer_ratio(data_file: str) -> dict:
    """
    This function calculates and returns the ratio of sales of each
    beer type as a dictionary.
    """
    ratio = {'Red Helles':0, 'Pilsner':0, 'Dunkel':0}
    red_helles = 0
    pilsner = 0
    dunkel = 0
    sales_file = pandas.read_csv(data_file)
    sales = sales_file.to_dict()

    # Increments the total bottles sold for each beer type.
    for sale in sales['Invoice Number']:
        if sales['Recipe'][sale] == 'Organic Red Helles':
            red_helles += sales['Quantity ordered'][sale]
        elif sales['Recipe'][sale] == 'Organic Pilsner':
            pilsner += sales['Quantity ordered'][sale]
        elif sales['Recipe'][sale] == 'Organic Dunkel':
            dunkel += sales['Quantity ordered'][sale]

    total = red_helles + pilsner + dunkel
    ratio['Red Helles'] = (red_helles/total)
    ratio['Pilsner'] = (pilsner/total)
    ratio['Dunkel'] = (dunkel/total)
    return ratio

def predictions(growth: float, bottles_sold: dict, ratio: list):
    """
    This function uses the values returned from the two functions above
    to calulate and return predictions on the volumes of each beer type
    and the data those volumes are predicted to be required.
    """
    BOTTLE_VOLUME = 0.5
    now = datetime.datetime.now()
    # Time 9 months before the current time.
    date_past = now - datetime.timedelta(9*365.25636/12)
    # Time 3 months after the current time.
    data_future = now + datetime.timedelta(3*365.25636/12)
    date_formatted = date_past.strftime('%b') + '-' + \
    date_past.strftime('%y')

    try:
        total_bottles = (bottles_sold[date_formatted] * (1 + growth))
    except:
        total_bottles = 0
    # Month and year the preducted volumes are required.
    month_required = [data_future.strftime('%B') + ' ' + \
    data_future.strftime('%Y'), date_past.strftime('%B') + ' ' + \
    date_past.strftime('%Y')]

    red_helles_bottles = ceil(total_bottles * ratio['Red Helles'])
    red_helles_volume = ceil(red_helles_bottles * BOTTLE_VOLUME)
    pilsner_bottles = ceil(total_bottles * ratio['Pilsner'])
    pilsner_volume = ceil(pilsner_bottles * BOTTLE_VOLUME)
    dunkel_bottles = ceil(total_bottles * ratio['Dunkel'])
    dunkel_volume = ceil(dunkel_bottles * BOTTLE_VOLUME)
    return (red_helles_volume, pilsner_volume, dunkel_volume, \
            month_required)

def get_evidence():
    """
    This function returns the data that was used to calculate the
    predicted volumes to enable the user to manually validate the
    predictions.
    """
    BOTTLE_VOLUME = 0.5
    data_evidence = []
    red_helles_bottles = 0
    pilsner_bottles = 0
    dunkel_bottles = 0
    now = datetime.datetime.now()
    now = now.month
    # Increments index of the current month by 3.
    if now == 11:
        now = 2
    elif now == 12:
        now = 3
    else:
        now += 3

    file = open('Barnabys_sales_fabriacted_data.csv')
    reader = csv.reader(file, delimiter=',')
    #https://evanhahn.com/python-skip-header-csv-reader/
    next(reader)
    for row in reader:
        date_required = datetime.datetime.strptime(row[2], '%d-%b-%y')
        if date_required.month == now:
            data_evidence.append(row)
    for sale in data_evidence:
        if sale[3] == 'Organic Red Helles':
            red_helles_bottles += int(sale[5])
        elif sale[3] == 'Organic Pilsner':
            pilsner_bottles += int(sale[5])
        elif sale[3] == 'Organic Dunkel':
            dunkel_bottles += int(sale[5])
    return data_evidence, ceil(red_helles_bottles*BOTTLE_VOLUME), \
           ceil(pilsner_bottles*BOTTLE_VOLUME), \
           ceil(dunkel_bottles*BOTTLE_VOLUME)
