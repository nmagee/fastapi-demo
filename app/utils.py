#!/usr/bin/env python3

import mysql.connector
from mysql.connector import Error

# DBHOST = "ds2022.cqee4iwdcaph.us-east-1.rds.amazonaws.com"
# DBUSER = "admin"
# DBPASS = os.getenv('DBPASS')
# DB = "nem2p"
# db = mysql.connector.connect(user=DBUSER, host=DBHOST, password=DBPASS, database=DB, ssl_disabled=True)
# cur = db.cursor()

class MySQLConnection:
    def __init__(self, host, user, password, database):
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.connection = None
        self.cursor = None

    def connect(self):
        try:
            self.connection = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database,
                ssl_disabled=True
            )
            self.cursor = self.connection.cursor()
            print("Connected to MySQL database successfully.")
        except mysql.connector.Error as err:
            print(f"Error: {err}")

    def close(self):
        if self.cursor:
            self.cursor.close()
        if self.connection:
            self.connection.close()
        print("MySQL connection closed.")

    def execute_query(self, query):
        self.connect()
        self.cursor.execute(query)
        result = self.cursor.fetchall()
        self.close()
        return result
