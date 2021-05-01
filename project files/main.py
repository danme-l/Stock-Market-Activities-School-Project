### DANIEL MELERAS - mele0036 - Final Version: April 14, 2021
### Project 2 for CST2101: Business Intelligence Programming
### --------------------------------------------------------------------
### This is the main file. Run this to launch the program
### --------------------------------------------------------------------


import tkinter as tk
from tkinter import ttk
from tkinter.messagebox import showinfo

from entry import EntryFrame, LeftPane
from display import DisplayFrame, RightPane
from data import DatabaseTools as dbt


if __name__ == "__main__":
    # create the database on program launch
    conn = dbt.create_connection(r'project.db')
    create_table_sql = '''CREATE TABLE IF NOT EXISTS stocks
             (date text, symbol text, trans text, quant real, price real)'''
        
    if conn is not None:
        dbt.create_table(conn, create_table_sql)

    else:
        print("Error! cannot create the database connection.")

    lpane = LeftPane()
    rpane = RightPane()

    EntryFrame(lpane)
    DisplayFrame(rpane)

    lpane.mainloop()  
    rpane.mainloop()