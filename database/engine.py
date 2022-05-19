import os
import sqlite3
import string
import random
import mysql.connector

from config import config

class DatabaseEngine:

    connection = None
    cursor = None

    @staticmethod
    def connect() -> None:
        """ Connect to the database file """
        
        DatabaseEngine.connection = mysql.connector.connect(
            host        = config["DATABASE_SERVER"],
            port        = config["DATABASE_PORT"],
            user        = config["DATABASE_USER"],
            password    = config["DATABASE_PASSWORD"],
            database    = config["DATABASE"]
        )
        
        DatabaseEngine.cursor = DatabaseEngine.connection.cursor() # Create new cursor object instance

    @staticmethod
    def disconnect() -> None:
        """ Close connection to the database file"""

        DatabaseEngine.connection.close()
        DatabaseEngine.connection = None
        DatabaseEngine.cursor = None

    @staticmethod
    def commit() -> None:
        """ Save changes to a database after a command has been executed """
        
        if not DatabaseEngine.connection: return # Dont commit if no connection is established
        DatabaseEngine.connection.commit()

    @staticmethod
    def gen_id() -> str:
        """ Generate a unique ID """
        # A unique ID consists of 32 randomly selected upper/lowecase letters and numbers

        ID = ""
        for x in range(32):
            ID += random.choice(list(string.ascii_letters + string.digits))

        return ID

    @staticmethod
    def id_exists(table:str, ID:str) -> bool:
        """ Check if ID already exists in a table """
        
        query = "SELECT ID FROM %s WHERE ID = %s;" # SQL query
        
        DatabaseEngine.connect() # Connect to the database
        data = DatabaseEngine.cursor.execute(query, (table, ID)).fetchone() # Execute the query and fetch one record
        DatabaseEngine.disconnect()

        if not data: return False # Return false if no data is found
        return True

