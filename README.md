# Stock-Market-Activities-School-Project
Algonquin CST2101: Project 2

This is the Second Project for CST 2101: Business Intelligence Programming.

# Design
The program is divided into 5 python files: main, entry, display, data

**main.py**

This file is the main file that runs the program. As soon as the program is run, the database is created, both window objects and both frames from the GUI are instantiated and the GUI is immediately opened (GUI details below).

**entry.py**

This file contains two classes. The first is the window object, which simply gives the activity entry window a size and title, and holds the frame.	The next is the EntryFrame class. The frame object will have two static attributes, one specifying the database created by the main file, and the other, the default message to display to the user, which just contains basic instructions on the date format. 

The __init__() method for the frame specifies some padding to pass to all attributes as kwargs, creates a list of entries to iterate over (this was needed by the clear() function, described below), and calls the create_widgets() method.

The create_widgets() method instantiates all the widgets described in the GUI documentation, and places them in the grid.
  
The record_data() method is meant to add records to the database. First, it retrieves the user-entered-data from the entries on the activity entry window. There is a try-except block that can catch value errors for the numeric attributes (quantity and price), and the user-entries are also validated with a specific function (described in the data file). If it’s valid, it creates a connection to the database, adds the record; otherwise, it displays a message to the user on the GUI.
  
The clear_entry() method simply empties the entries by iterating over the list of entries and calling the entry.delete() method. It also returns the label with messages for the user to the original state.
  
The search() method functions almost the record_data() method except that instead of adding the data to the database, it checks the database for the record entered by the user. If it’s there, it will display it, otherwise it will display a message indicating its absence.
  
The export() method connects to the database and writes the contents of it to a text file. It also displays a confirmation message to the user on the GUI.
  
**display.py**

Similarly to the entry.py file, this file contains two classes: the first is the window object, which simply gives the activity display a size and title, and holds the frame.

The other is the DisplayFrame class. Here, all the widgets were created directly in the __init__() method. First, there is a sub-frame here to hold the buttons, so that they could be placed in the same cell in the grid. The buttons are then added to that sub-frame, which is in turn added to the main window. This was so I could use the pack geometry manager on the buttons but keep the grid geometry manager for the rest of the window.

The display_activities() connects to the database and retrieves a string of all the records therein, then displays them on the GUI.

The display_summary() method connects to the database and then calls each relevant method from the DatabaseTools class in data.py one by one. It then formats the output of those methods into a string, to be displayed to the user on the GUI. The information displayed on the summary, as described on the project specifications, is as follows:
* Oldest Transaction Date (should display name of stock transacted as well. If more than one stock then display just one name)
* Newest Transaction Date (should display name of stock transacted as well. If more than one stock then display just one name)
*	Number of unique stock symbols in all activities (list them)
*	The cheapest price paid for any stock (should display name of stock transacted as well. If more than one stock then display just one name)
*	The most expensive price paid for any stock (should display name of stock transacted as well. If more than one stock then display just one name)
*	The stock symbol for the most traded stock
* The stock with the highest volume
The method also updates the label on the GUI to display the summary to the user.

This file also includes a main function to launch this window on it’s own, as figuring out the geometry took a significant amount of trial and error.

**data.py**

This file contains a single class, DatabaseTools, which contains all the relevant methods for manipulating the database. They are entirely static methods.
  
* create_connection() takes a string database file and tries to create a connection to it; if successful, the connection is returned, otherwise it returns None.
*	create_table() takes a connection object and a table creation command. It tries to connect, and if successful, creates the database.
*	push() takes a connection object and a record, in a tuple, to be inserted into the database. It tries to connect, and if successful, adds the record to the database.
*	display_all() takes a connection object, tries to connect, and if successful, combines all records in the database into a single string and returns it.
*	display_record() takes a connection object and a record. It tries to connect, and if successful, combines all records in the database  that match the input record into a single string and returns it.
*	display_oldest_trans() takes a connection object, tries to connect, and if successful, returns a tuple with the symbol and the date of the oldest transaction.
*	display_newest_trans() takes a connection object, tries to connect, and if successful, returns a tuple with the symbol and the date of the newest transaction.
*	display_unique_symbols() takes a connection object, tries to connect, and if successful, returns a tuple with all of the unique symbols in the database.
*	display_cheapest() takes a connection object, tries to connect, and if successful, returns a tuple with symbol and price of the cheapest stock in the database.
*	display_expensivest() takes a connection object, tries to connect, and if successful, returns a tuple with symbol and price of the most expensive stock in the database (yes, expensivest is a joke)
*	display_most_traded() takes a connection object, tries to connect, and if successful, returns a tuple of tuples, where all of the symbols and the number of times traded (a tuple) are ordered by number of times traded.
*	display_highest_volume() takes a connection object, tries to connect, and if successful, returns a tuple with symbol and quantity of the most traded stock in the database, using an SQL subquery.
*	record_to_string() takes a database record tuple and converts it to a string.
*	validate_entry() takes a record and creates a flag Boolean. It then validates the attributes one-by-one, to ensure that: (1) The date is the right format, validated by regular expressions; (2)	The symbol is fewer than 8 characters long and only contains letters and a period, so that symbols on multiple exchanges can be entered (VUN vs VUN.TO, for example); (3)	The transaction is only ‘BUY’ or ‘SELL’ (not case-sensitive); (4)	The quantity is an integer, and (5) The price is an integer or a float.

# GUI
The program features a GUI built entirely with the tkinter library. It is divided in two: An Activity Entry and an Activity Display.

**Activity Entry**

The activity entry is entirely defined in the entry.py class. There is a window object with a frame inside it that uses the grid geometry organizer. 

The widgets are initialized within a create_widgets() function, to create each of the following widgets, from top to bottom on the display:
*	Each record in the database needs to have five attributes (date, symbol, transaction, quantity, price) so the function makes label and entry widgets for each of those. 
*	Below that, there will be three buttons: one for recording information from the entries into the database; one for clearing the user input from the entries; one for searching the database for the information in the entries.
*	Under the buttons, there is a label that displays one of the following messages to the user:
  -	The record that was searched for, if the user is searching;
  -	An appropriate message if no record was found was found; 
  -	The record that was added, as well as a confirmation message, if the record was successfully added to the database;
  -	An appropriate message if the record could not be added to the database.
*	Finally, there is a button to export the entire database into a text file, as well as a label to display a confirmation message.

**Activity Display**

The activity display is entirely defined the display.py class. Just like above, there is a window object with a frame inside it that uses the grid geometry organizer. 
*	This frame has a subframe to contain the two buttons; this way, both buttons could be placed inside a single cell of the grid. 
*	Underneath that, there is a display that updates itself with the appropriate text based on whichever button the user clicked:
  -	Summary: a summary of the entries, according to the project spec.
  -	Activities: all activities in chronological order.
