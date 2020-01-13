# Barnaby's Brewhouse

This software is designed to be run by the employees of Barnaby's Brewhouse.


## What can you do in this program?

This program enables you to:
• Upload new sales files which are saved and used for prediction calculations. This can be done in the first column 'Update System' at the top with the title 'Upload Sales Data'.
• Upload new batches of beer to the system. This can be done in the first column 'Update System' in the middle with the title 'Upload New Batch'.
• Upload new Customer Orders to the system and dispatch them. This can be done in the first column at the bottm with the title 'Upload New Customer Order'.
• Change the phase of a batch. This can be done in the first column in the middle with the title 'Batches'.
• Update the stock manually of each type of beer in case there is an error or a customer has returned their order. This can be done in the second column 'Production Management' at the top with the title 'Update Stock Manually'.


## What does this program display?

• The first column 'Update System' will display a table of all batches that are currently being processed. It also displays a table of all customer orders that are waiting to be dispatched along with information such as the date required, type of beer and quantity of bottles.
• The second column 'Production Management' will display your current inventory of Red Helles, Pilsner and Dunkel. It will also display the status of each tank. If a tank is empty it is marked as empty, if there is a batch inside the details of the batch and phase of that batch are displayed as well as a progress bar to see how full the tank.
• The third column 'Predictions' will help you decide the volume of each beer that will be needed 3 months from now and which beer is best to brew next with reasons as to why. The quantity required at the same time last year will also be displayed just above a table of data that was used for these predictions to enable you to validate the predictions.


## How do I run this program?

1. If you do not already have python installed, click this [link](https://www.python.org/downloads/),   download and install the lastest version of Python 3 for Windows. This software has been tested on   3.7.4 and 3.8.0.
2. Drag the Barnaby's Brewhouse folder from your downloads folder to the desktop.
3. Open the folder, click on the folder name to the left of the search bar and copy the file path.
4. Type in the windows search bar 'Command Prompt' and open the program.
5. Type 'pip install pandas', press enter and wait for the libary to install.
6. Type 'cd ', paste the file path and press enter.
7. Type 'python barnabys_brewhouse.py' and press enter.
8. The following text should appear:

* Serving Flask app "barnabys_brewhouse" (lazy loading)
* Environment: production
WARNING: This is a development server. Do not use it in a production deployment.
Use a production WSGI server instead.
* Debug mode: on
* Restarting with stat
* Debugger is active!
* Debugger PIN: 308-925-164
* Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)

9. Copy the website link on the last line of your command prompt and paste it into a web browser (Chrome is recommended). The interface should appear in the browser and the program is running.
