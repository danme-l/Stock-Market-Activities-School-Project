### DANIEL MELERAS - mele0036 - Final Version: April 14, 2021
### Project 2 for CST2101: Business Intelligence Programming
### --------------------------------------------------------------------------
### This file has a single class to manipulate the database with helper 
### functions as static methods.
### --------------------------------------------------------------------------

import sqlite3 as sq
from sqlite3 import Error
import os
import re

class DatabaseTools:
    """ Helper methods for manipulating the database
        NOTE: much of this code is lifted directly from the Week 10 notes """

    @staticmethod
    def create_connection(db_file):
        """ create a database connection to the SQLite database specified by db_file
        """
        conn = None
        try:
            conn = sq.connect(db_file)
            return conn
        except Error as e:
            print(e)

        return conn
    
    @staticmethod
    def create_table(conn, create_table_sql):
        """ create a table from the passed in create_table_sql statement
        """
        try:
            c = conn.cursor()
            c.execute(create_table_sql)
        except Error as e:
            print(e)

    @staticmethod
    def push(conn, record):
        """Creates a cursor object, executes the INSERT statement, commites changes"""

        insert_command = '''INSERT INTO stocks(date, symbol, trans, quant, price) VALUES(?,?,?,?,?)'''

        try:
            c=conn.cursor()
            c.execute(insert_command, record)
            conn.commit()
        except Error as e:
            print(e)

    @staticmethod
    def display_all(conn):
        """Creates a cursor object, executes the SELECT statement, returns results in a string"""
        retString = ""
        
        try:
            c = conn.cursor()
            c.execute("SELECT * FROM stocks ORDER BY date")

            # iterates over all the rows returns by the select statement
            rows = c.fetchall()
            for row in rows: 
                retString += DatabaseTools.record_to_string(row) + '\n'

        except Error as e:
            print(e)


        return retString

    @staticmethod
    def export_all(conn):
        """Creates a cursor object, executes the SELECT statement, returns results in a string"""
        
        retString = ""
        
        try: 
            c = conn.cursor()
            c.execute("SELECT * FROM stocks ORDER BY date")    

            # iterates over all the rows returns by the select statement
            rows = c.fetchall()
            for row in rows: 
                retString += 'User Activity: ' + DatabaseTools.record_to_string(row) + '\n'
        except Error as e:
            print(e)

        return retString

    @staticmethod
    def display_record(conn, record):
        """Creates a cursor object, executes the SELECT statement, 
        puts results into a string if there are any, returns it"""

        retString = ""           

        select_command = """SELECT * FROM stocks WHERE 
                        date=? AND
                        symbol=? AND 
                        trans=? AND 
                        quant=? AND 
                        price=? """

        try:
            c=conn.cursor()   
            c.execute(select_command, record)


            rows = c.fetchall()
            if rows: # non-empty rows evaluate to true
                for row in rows:  # print every matching record
                    retString += DatabaseTools.record_to_string(row) + '\n'
            else:
                retString = "Not found."
        except Error as e:
            print(e)

        return retString

    @staticmethod
    def display_oldest_trans(conn):
        """Creates a cursor object, executes the SELECT statement to find oldest date, 
        puts date and symbol into a string, returns it"""
        try:
            c = conn.cursor()
            c.execute("""SELECT symbol, MIN(date) FROM stocks""")
        except Error as e:
            print(e)         

        # tuple of symbol and the earliest date
        return c.fetchone()

    @staticmethod
    def display_newest_trans(conn):
        """Creates a cursor object, executes the SELECT statement to find newest date, 
        puts date and symbol into a string, returns it"""
        try:
            c = conn.cursor()
            c.execute("""SELECT symbol, MAX(date) FROM stocks""")
        except Error as e:
            print(e)     
                
        # tuple of symbol and the most recent date
        return c.fetchone()

    @staticmethod
    def display_unique_symbols(conn):
        """Creates a cursor object, executes the SELECT statement to
        find all unique symbold in the database, puts them in a tuple, returns it"""
        try:
            c = conn.cursor()
            c.execute("""SELECT DISTINCT symbol FROM stocks""")
        except Error as e:
            print(e)
            
        # tuple of all the distinct symbols
        return c.fetchall()

    @staticmethod
    def display_cheapest(conn):
        """Creates a cursor object, executes the SELECT statement to
        find cheapest transaction in the database, puts symbol and 
        price in a tuple, returns it"""
        try:
            c = conn.cursor()
            c.execute("""SELECT symbol, MIN(price) FROM stocks""")
        except Error as e:
            print(e)                
         
        # tuple of the symbol and price for the cheapest stock
        return c.fetchone()

    @staticmethod
    def display_expensivest(conn):
        """Creates a cursor object, executes the SELECT statement to
        find most expensive transaction in the database, puts symbol and 
        price in a tuple, returns it"""
        try:
            c = conn.cursor()
            c.execute("""SELECT symbol, MAX(price) FROM stocks""")
        except Error as e:
            print(e)

        # tuple of the symbol and price for the most expensive stock
        return c.fetchone() 

    @staticmethod
    def display_most_traded(conn):
        """Creates a cursor object, executes the SELECT statement to
        order all the trades in the database by most traded, puts all of them
        and the number of trades in a tuple, returns it"""
        try:   
            c = conn.cursor()
        
            # order all the symbols by number of trades
            c.execute(""" SELECT symbol, COUNT(symbol)
                    FROM stocks
                    GROUP BY symbol
                    ORDER BY COUNT(symbol) DESC""")
        except Error as e:
            print(e)
                  
        # tuple of symbol and number of trades for most traded stock
        return c.fetchall()

    @staticmethod
    def display_highest_volume(conn):
        """Creates a cursor object, executes the SELECT statement to
        find most symbol with the highest trade volume in the database, puts symbol and 
        quantity in a tuple, returns it"""
        try:   
            c = conn.cursor()
        
            # subquery gets all the symbols and their total trade volume
            # main query extracts the one with the max
            c.execute(""" SELECT symbol, MAX(tradesum)
                    FROM
                    (SELECT symbol, SUM(quant) AS "tradesum"
                     FROM stocks
                     GROUP BY symbol)""")
        except Error as e:
            print(e) 

        # tuple of symbol and number of trades for most traded stock
        return c.fetchall()

    @staticmethod
    def record_to_string(record):
        """ Converts a database record tuple to a string
            All database records will have length 5"""
        return (str(record[0]) + ' ' +      # date
                record[1].upper() + ' ' +   # symbol
                record[2].upper() + ' ' +   # transaction
                str(record[3]) + ' ' +      # quantity
                '$' + str(record[4]))       # price

    @staticmethod
    def validate_entry(record):
        # flag
        f = False
        
        # date validation
        if re.search(r'[\d]{4}-[\d]{1,2}-[\d]{1,2}', record[0]):
            f = True
        else:
            print("date failure")
            return False # wrong date format
    
        # symbol validation
        if len(record[1]) < 8:  # symbols can be up to 7 chars: wxyz.to
            for c in record[1]:
                if c.isalpha() or c == '.':
                    f = True 
                else:
                    print("symbol val failure")
                    return False # symbol has invalid char
        else:
            print("symbol len failure")
            return False # symbol too short

        # transaction validation
        if record[2].lower() == 'buy' or record[2].lower() == 'sell':
            f = True
        else:
            print("trans failure")
            return False # invalid transaction type

        # quantity validation
        if type(record[3]) == int: # can't have decimal quantities
            if record[3] >= 0:
                f = True
        else:
            print("quantity failure")
            return False 

        # price validation
        if type(record[4]) == int or type(record[4]) == float:
            if record[4] > 0:
                f = True
        else:
            print("price failure")
            return False 


        return f
    
