### DANIEL MELERAS - mele0036 - Final Version: April 14, 2021
### Project 2 for CST2101: Business Intelligence Programming
### --------------------------------------------------------------------------
### This is for the Right Pane, which has the activities and summary functions
### There's a window object with an internal 
### frame. Both are instantiated by the main program, however this file
### includes a main function for testing purposes, as extensive testing 
### through trial and error was required.
### --------------------------------------------------------------------------

import tkinter as tk
from tkinter import ttk
from tkinter.messagebox import showinfo
from data import DatabaseTools as dbt

# main window object for the display window
class RightPane(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title('Activity Display')
        self.geometry('425x550+700+200')
        self.resizable(False, False)

# frame that goes within the window
class DisplayFrame(ttk.Frame):
    DATABASE = r'project.db'

    def __init__(self,container):
        super().__init__(container)

        options = {'padx': 5, 'pady': 5}
        
        # show the frame on the container
        self.pack(**options)

        # configure grid
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.columnconfigure(2, weight=1)

        # make a subframe for the buttons
        # so they could be in a single cell in the grid
        # otherwise if the column underneath a button expanded 
        # when it changed size to accomodate text the buttons would move.
        buttonframe = tk.Frame(self)

        summary_button = ttk.Button(buttonframe, text='Summary', command=self.display_summary)
        summary_button.pack(side='left', padx=20, pady=10)

        activities_button = ttk.Button(buttonframe, text='Activities', command=self.display_activities)
        activities_button.pack(side='right', padx=20, pady=10)

        # place the buttonframe sub-frame in the grid
        buttonframe.grid(column=1, row=0)

        # display label (goes into the main frame)
        self.display_label = ttk.Label(self, wraplength=300)
        self.display_label.grid(column=1, row=3, sticky=tk.W, **options)




    def display_activities(self):
        """Connects to the database, retrieves all the records, displays them"""
        # connect to the database to search for the record
        conn = dbt.create_connection(self.DATABASE)
        displayString = dbt.display_all(conn)

        # updates results label with the search results
        self.display_label.config(text=displayString)

    def display_summary(self):
        """Connects to the database and calls the relevant function from DatabaseTools class
            puts each result into a string that are amalgamated together and displayed on the frame"""
        # connect to the database
        conn = dbt.create_connection(self.DATABASE)

        # displays
        oldestTrans = dbt.display_oldest_trans(conn) # gets first date and symbol

        newestTrans = dbt.display_newest_trans(conn) # gets last date and symbol
        
        uniqueSymbolsTup = dbt.display_unique_symbols(conn) # gets tuple of unique symbols
        # arrange the symbols into a string
        uniqueSymbols = ''
        for s in uniqueSymbolsTup:
            uniqueSymbols += s[0] + ', '

        cheapest = dbt.display_cheapest(conn) # gets cheapest price paid and symbol

        expensive = dbt.display_expensivest(conn) # gets highest price paid and symbol

        mostTradedTup = dbt.display_most_traded(conn) # orders stocks by times traded
        try:
            mostTraded = [mostTradedTup[0]]      # formats all the stocks with most trades for displaying
            for sym, num in mostTradedTup[1:]:
                if num < mostTradedTup[0][1]:
                    break
                mostTraded.append((sym, num))
        except IndexError:
            pass

        
        # note: this is included since the first time I submitted, I mistakenly thought
        # the spec was asking for volume, not number of trades
        highestVolume = dbt.display_highest_volume(conn) # gets stock with highest trade volume

        # format the string to display
        try:
            displayString = ""
            displayString += "Oldest Transaction Date: " + oldestTrans[0] + " on " + oldestTrans[1] + '\n\n'
            displayString += "Newest Transaction Date: " + newestTrans[0] + " on " + newestTrans[1] + '\n\n'
            displayString += "Unique Symbols Traded:\n  " + uniqueSymbols[:-2] + '\n\n' # remove trailing space and comma
            displayString += "Cheapest Stock Traded: " + cheapest[0] + " for $" + str(cheapest[1]) + '\n\n'
            displayString += "Most Expensive Stock Traded: " + expensive[0] + " for $" + str(expensive[1]) + '\n\n'
            
            # handle the case where more than one have been traded the same, max number of time
            if len(mostTraded) == 1:
                displayString += "Most Traded Stock: " + mostTraded[0][0] + " has been traded " + str(mostTraded[0][1]) + " times.\n\n"
            else:
                displayString += "Most Traded Stocks:" 
                for sym, num in mostTraded:
                    displayString += sym + ", "
                displayString = displayString[:-2] # remove trailing space and comma
                displayString += " have been traded " + str(mostTraded[0][1]) + " times.\n\n"
            
            displayString += "Stock with highest Trade Volume: " + str(highestVolume[0][1]) + " total shares of " + highestVolume[0][0] + " have been traded.\n\n"
        except TypeError:
            displayString = "Database is empty."

        # update the frame with the display
        self.display_label.config(text=displayString)


# for testing purposes
if __name__ == "__main__":
    app = RightPane()
    DisplayFrame(app)
    app.mainloop()


