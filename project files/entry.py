### DANIEL MELERAS - mele0036 - Final Version: April 14, 2021
### Project 2 for CST2101: Business Intelligence Programming
### -----------------------------------------------------------------------------
### This is for the Left window, the entry window which contains the input boxes.
### This Window gives the user the ability to store and search for transactions
### in the database, as well as a button to clear the boxes.
### -----------------------------------------------------------------------------

import tkinter as tk
from tkinter import ttk
from tkinter.messagebox import showinfo
from data import DatabaseTools as dbt

# main window object for the entry window
class LeftPane(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title('Activity Entry')
        self.geometry('450x550')
        self.resizable(False, False)

# frame that goes within the window
class EntryFrame(ttk.Frame):
    
    DATABASE = r'project.db'
    FORMAT_INS = 'Please enter date in YYYY-DD-MM format.\n'

    def __init__(self, container):
        super().__init__(container)

        # field options
        options = {'padx': 5, 'pady': 5}

        # list of entries to iterate over
        self.entries = []

        # create the widgets when this frame is initialized
        self.create_widgets(options)

    def create_widgets(self, options):
        """ Initiates all the widgets to go into the Entry Frame
            adds them the entries to the entries list"""

        # Date label/entry
        self.date_label = ttk.Label(self, text='Date')
        self.date_label.grid(column=0, row=0, sticky=tk.W, **options)
        
        self.date = tk.StringVar()
        self.date_entry = ttk.Entry(self, textvariable=self.date, width=10)
        self.date_entry.grid(column=0, row=1, **options)
        self.date_entry.focus()
        self.entries.append(self.date_entry)

        # Symbol label/entry
        self.symbol_label = ttk.Label(self, text='Symbol')
        self.symbol_label.grid(column=1, row=0, sticky=tk.W, **options)
        
        self.symbol = tk.StringVar()
        self.symbol_entry = ttk.Entry(self, textvariable=self.symbol, width=10)
        self.symbol_entry.grid(column=1, row=1, **options)
        self.symbol_entry.focus()
        self.entries.append(self.symbol_entry)

        # Transaction label/entry
        self.trans_label = ttk.Label(self, text='Transaction')
        self.trans_label.grid(column=2, row=0, sticky=tk.W, **options)

        self.trans = tk.StringVar()
        self.trans_entry = ttk.Entry(self, textvariable=self.trans, width=10)
        self.trans_entry.grid(column=2, row=1, **options)
        self.trans_entry.focus()
        self.entries.append(self.trans_entry)

        # Quantity label/entry
        self.quantity_label = ttk.Label(self, text='Quantity')
        self.quantity_label.grid(column=3, row=0, sticky=tk.W, **options)

        self.quantity = tk.StringVar()
        self.quantity_entry = ttk.Entry(self, textvariable=self.quantity, width=10)
        self.quantity_entry.grid(column=3, row=1, **options)
        self.quantity_entry.focus()
        self.entries.append(self.quantity_entry)

        # Price label/entry
        self.price_label = ttk.Label(self, text='Price')
        self.price_label.grid(column=4, row=0, sticky=tk.W, **options)

        self.price = tk.StringVar()
        self.price_entry = ttk.Entry(self, textvariable=self.price, width=10)
        self.price_entry.grid(column=4, row=1, **options)
        self.price_entry.focus()
        self.entries.append(self.price_entry)

        # buttons
        self.record_button = ttk.Button(self, text='Record', command=self.record_data)
        self.record_button.grid(column=1, row=2, sticky=tk.W, **options)

        self.clear_button = ttk.Button(self, text='Clear', command = self.clear_entries)
        self.clear_button.grid(column=2, row=2, sticky=tk.W, **options)

        self.search_button = ttk.Button(self, text='Search', command = self.search)
        self.search_button.grid(column=3, row=2, sticky=tk.W, **options)

        # result label
        self.result_label = ttk.Label(self, text=self.FORMAT_INS)
        self.result_label.grid(column=0, row=5, columnspan=3,sticky=tk.W, **options)

        # export button/label
        self.export_button = ttk.Button(self, text="Export to \ntext file", command = self.export)
        self.export_button.grid(column=0, row=6, sticky=tk.W, **options)

        self.export_label = ttk.Label(self)
        self.export_label.grid(column=0, row=7, columnspan=3, sticky=tk.W, **options)

        # add padding to the frame and show it
        self.grid(padx=10, pady=10, sticky=tk.NSEW)

    def record_data(self):
        """Retrieves data from entry boxes, connects to the database and inserts it"""

        # get the data from the entries
        date = self.date_entry.get()
        symbol = self.symbol_entry.get()
        trans = self.trans_entry.get()
        quant = self.quantity_entry.get()
        price = self.price_entry.get()

        # the try-except block can catch value errors
        # checks entry formatting with a database validation function
        try: 
            record = (date, symbol.upper(), trans.upper(), int(quant), float(price))
            
            # check with validation function
            if dbt.validate_entry(record):

                # connect to the database and push it in
                conn = dbt.create_connection(self.DATABASE)
                dbt.push(conn, record)

                # updates results label with the add results
                self.result_label.config(text=self.FORMAT_INS + 'Record Added: \n' + dbt.record_to_string(record))

            else:
                self.result_label.config(text=self.FORMAT_INS + 'Invalid Entry.')

        except ValueError:
            self.result_label.config(text=self.FORMAT_INS + 'Invalid Entry.')
    
    def clear_entries(self):
        """loop over the entries and delete what's in the box"""
        for entry in self.entries:
            entry.delete(0, 'end')
        
        # return the results label to original state
        self.result_label.config(text=self.FORMAT_INS)

    def search(self):
        """Retrieves data from entry boxes, connects to the database and searches for it"""
        date = self.date_entry.get()
        symbol = self.symbol_entry.get()
        trans = self.trans_entry.get()
        quant = self.quantity_entry.get()
        price = self.price_entry.get()

        # the try-except block can catch value errors
        # checks entry formatting with a database validation function
        try: 
            record = (date, symbol.upper(), trans.upper(), int(quant), float(price))
            
            # check with validation function
            if dbt.validate_entry(record):
                # connects to the database to search for the record
                conn = dbt.create_connection(self.DATABASE)
                displayString = dbt.display_record(conn, record)

                # updates results label with the search results
                self.result_label.config(text=self.FORMAT_INS + 'Record: \n' + displayString)

            else:
                self.result_label.config(text=self.FORMAT_INS + 'Invalid Entry.')

        except ValueError:
            self.result_label.config(text=self.FORMAT_INS + 'Invalid Entry.')

    def export(self):
        """Exports contents of the Database to a text file"""
        conn = dbt.create_connection(self.DATABASE)

        text = dbt.export_all(conn)
        tfile = open("activities.txt", "w")
        tfile.write(text)
        tfile.close()

        # update GUI with confirmation message
        self.export_label.config(text="Exported to activities.txt")

