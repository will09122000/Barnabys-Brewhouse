"""
This program provides multiple features to make processing beer and
decision making easier for Barnaby's Brewhouse. The program will enable
them to: Upload sales data to be used to influence the planning
decisions on which beer to brew next with reasoning. Upload a new batch
of beer with the choice of a tank preference and if not the most
suitable tank is automatically picked displaying all batches
currently being processed. Upload new customer orders and
dispatch them. Displays current inventory of each beer enabling them to
update the stock manually in case beers are returned or other
unforeseen circumstances. Displays the status of each tank with details
of the batch inside each tank. Recommends the beer to be added to the
batch queue next based on various factors such as current stock and
tank status. Provides an estimate on the volume of each beer that will
be required 3 months from now with evidence from the same month last
year.
"""
import datetime
import csv
from flask import Flask, render_template, redirect, request
from sales_predictions import growth_rate, get_beer_ratio, \
predictions, get_evidence
from tank_management import get_tank_status
from inventory import get_inventory, update_inventory
from batch_management import add_new_batch, next_phase, get_batches
from order_management import order_bottles, get_orders, dispatch_order
from beer_suggestion import suggest_beer
from logs import log_info

stock_monitor = Flask(__name__)

@stock_monitor.route('/', methods=['GET', 'POST'])
def home():
    """
    This function is responsible for fetching: the growth rate, total
    bottles sold and the beer type ratio of bottles sold from the
    given sales data. The predicted volumes required 3 months from now
    as well as the evidence for that prediction. Lastly, the current
    date. This data is fetched to be displayed on the main page.
    """
    growth, bottles_sold = growth_rate \
    ('Barnabys_sales_fabriacted_data.csv')
    ratio = get_beer_ratio('Barnabys_sales_fabriacted_data.csv')
    rh_volume, p_volume, d_volume, month_required = \
    predictions(growth, bottles_sold, ratio)
    data_evidence, rh_vol_evidence, p_vol_evidence, d_vol_evidence \
    = get_evidence()
    next_beer, inventory_reason, batch_reason, ratio_reason = \
    suggest_beer()
    # Current day used to prevent the user from uploading a new
    # customer order with a date required in the past.
    now = datetime.datetime.now()

    return render_template('index.html', rh_volume=rh_volume,
                           p_volume=p_volume, d_volume=d_volume,
                           month_required=month_required,
                           data_evidence=data_evidence,
                           rh_vol_evidence=rh_vol_evidence,
                           p_vol_evidence=p_vol_evidence,
                           d_vol_evidence=d_vol_evidence,
                           tank_status=get_tank_status(),
                           inventory=get_inventory(),
                           batches=get_batches(),
                           orders=get_orders(),
                           next_beer=next_beer,
                           inventory_reason=inventory_reason,
                           batch_reason=batch_reason,
                           ratio_reason=ratio_reason,
                           today=now.strftime('%Y-%m-%d')
                           )

@stock_monitor.route('/add-sales-data', methods=['GET', 'POST'])
def add_sales_data_function():
    """
    This function handles new sales files being uploaded by the user
    via the user interface. It will check that it is a valid csv file
    with the correct headers, then it will re-calculate the predictions
    data based on the new file as well as all existing data. 
    """
    if request.method == 'POST':
        if 'sales_file' not in request.files:
            error = 'Unkown error'
            return render_template('invalid_csv.html', error=error)
        sales_file = request.files['sales_file']
        if sales_file.filename == '':
            error = "Please click the 'Choose file' button to select \
                    the csv sales data file you would like to \
                    upload. Then press the 'Upload' button. Press \
                    'Back' to return to the main page."
            return render_template('invalid_csv.html', error=error)
        if sales_file.filename[-3:] != 'csv':
            error = "Please make sure you are uploading the correct \
                    file, it should end with the file extension: \
                    '.csv'. Press 'Back' to return to the main page."
            return render_template('invalid_csv.html', error=error)
        sales_file.save(sales_file.filename)

        # Opens the uploaded file and checks the headers are correct.
        with open(sales_file.filename,'r') as new_sales_file:
            new_sales = csv.reader(new_sales_file)
            header = (str(next(new_sales)))
            if header == "['Invoice Number', 'Customer', 'Date Required', 'Recipe', 'Gyle Number', 'Quantity ordered']":
                # Appends new lines to existing sales data file.
                with open('Barnabys_sales_fabriacted_data.csv', \
                        'a',newline='') as sales_file:
                    sales = csv.writer(sales_file)
                    for sale in new_sales:
                        sales.writerow(sale)
                log_info('New sales data added.')
                return redirect('/')
            else:
                error = "Incorrect CSV file formatting. Please make sure \
                        the top row of the file is: 'Invoice Number, \
                        Customer,Date Required,Recipe,Gyle Number, \
                        Quantity ordered'. Also check that the sales \
                        below the top line are formatted like this: \
                        '228,Fermoys Garden Centre,06-Dec-18, \
                        Organic Red Helles,100,30'"
                return render_template('invalid_csv.html', error=error)

@stock_monitor.route('/add-new-batch', methods=['GET'])
def add_new_batch_function():
    """
    See 'add_new_batch()' in 'batch_management.py' for more
    information.
    """

    if request.method == 'GET':
        add_new_batch()
        return redirect('/')

@stock_monitor.route('/next-phase', methods=['GET'])
def next_phase_function():
    """
    See 'next_phase()' in 'batch_management.py' for more information.
    """
    if request.method == 'GET':
        next_phase()
        return redirect('/')

@stock_monitor.route('/add-new-order', methods=['GET'])
def add_new_order_function():
    """
    See 'order_bottles()' in 'order_management.py' for more
    information.
    """
    if request.method == 'GET':
        order_bottles()
        return redirect('/')

@stock_monitor.route('/dispatch-order', methods=['GET'])
def dispatch_order_function():
    """
    See 'dispatch_order()' in 'order_management.py' for more
    information.
    """
    if request.method == 'GET':
        dispatch_order()
        return redirect('/')

@stock_monitor.route('/update-stock', methods=['GET'])
def update_inventory_function():
    """
    See 'update_inventory()' in 'inventory.py' for more information.
    """
    if request.method == 'GET':
        update_inventory()
        return redirect('/')

if __name__ == '__main__':
    stock_monitor.run()
