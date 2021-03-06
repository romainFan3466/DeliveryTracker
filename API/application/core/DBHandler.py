
##############################################################################
# Context manager for connecting/disconnecting to a database.
##############################################################################

import mysql.connector
from flask import abort


class DBHandler:

    config=""
    conn = ""
    cursor=""

    def __init__(self, configuration:dict):
        self.config = configuration



    def __enter__(self):
        self.conn = mysql.connector.connect(**self.config)
        self.cursor = self.conn.cursor(dictionary=True)
        return self.cursor



    def __exit__(self, exc_type, exc_value, exc_traceback):
        self.cursor.close()
        self.conn.commit()
        self.conn.close()



    def query(self, sql:str, params:dict=None, multiple=True, fetch=True):
        try:
            self.conn = mysql.connector.connect(**self.config)
            self.cursor = self.conn.cursor(dictionary=True)
            self.cursor.execute(sql, params)

            rows = []
            if fetch is True:
                rows = self.cursor.fetchall() if multiple is True else self.cursor.fetchone()

            self.cursor.close()
            self.conn.commit()
            self.conn.close()

            return rows
        except mysql.connector.Error as err:
            print("Something went wrong: {}".format(err))
            abort(500)



    def select(self, table, selected_columns:tuple=("*",), conditions:dict=None, multiple=True):
        try:
            self.conn = mysql.connector.connect(**self.config)
            self.cursor = self.conn.cursor(dictionary=True)

            selected_column_names = ", ".join(str(column) for column in selected_columns)
            columns= " AND ".join(key + "= %(" + key +")s" for key, value in conditions.items()) if conditions is not None else "1"

            sql = ("SELECT "+ selected_column_names +" FROM "+ table + " WHERE "+ columns + ";")

            self.cursor.execute(sql, conditions)

            rows = self.cursor.fetchall() if multiple is True else self.cursor.fetchone()

            self.cursor.close()
            self.conn.commit()
            self.conn.close()

            return rows
        except mysql.connector.Error as err:
            print("Something went wrong: {}".format(err))
            abort(500)



    def insert(self, table, params:dict):
        try:
            self.conn = mysql.connector.connect(**self.config)
            self.cursor = self.conn.cursor(dictionary=True)
            columns= ", ".join("%("+ key + ")s" for key, value in params.items())
            column_names= ", ".join(key for key, value in params.items())
            sql = ("INSERT INTO "+ table + " (" + column_names + ") VALUES (" + columns +");")
            self.cursor.execute(sql, params)
            id = self.cursor.lastrowid

            self.cursor.close()
            self.conn.commit()
            self.conn.close()

            return id
        except mysql.connector.Error as err:
            print("Something went wrong: {}".format(err))
            abort(500)



    def update(self, table, params:dict, conditions:dict):
        try:
            self.conn = mysql.connector.connect(**self.config)
            self.cursor = self.conn.cursor(dictionary=True)
            params_columns= ", ".join(key + "= %(" + key +")s" for key, value in params.items())
            cond_columns = " AND ".join(key + "= %(" + key +")s" for key, value in conditions.items())
            sql = ("UPDATE "+ table + " SET "+ params_columns + " WHERE "+ cond_columns + ";")

            # merge 2 dicts
            params.update(conditions)

            self.cursor.execute(sql, params)
            self.cursor.close()
            self.conn.commit()
            self.conn.close()

            return True
        except mysql.connector.Error as err:
            print("Something went wrong: {}".format(err))
            abort(500)



    def delete(self, table, conditions:dict=None):
        try:
            self.conn = mysql.connector.connect(**self.config)
            self.cursor = self.conn.cursor(dictionary=True)

            columns= " AND ".join(key + "= %(" + key +")s" for key, value in conditions.items())

            sql = ("DELETE FROM "+ table + " WHERE "+ columns + ";")

            self.cursor.execute(sql, conditions)

            self.cursor.close()
            self.conn.commit()
            self.conn.close()

            return True
        except mysql.connector.Error as err:
            print("Something went wrong: {}".format(err))
            abort(500)



    def is_existing(self, table, conditions:dict):
        try:
            self.conn = mysql.connector.connect(**self.config)
            self.cursor = self.conn.cursor(dictionary=True)
            columns= " AND ".join(key + "= %(" + key +")s" for key, value in conditions.items())

            sql = ("SELECT 1 FROM "+ table + " WHERE "+ columns + ";")
            self.cursor.execute(sql, conditions)

            existing = self.cursor.fetchone()

            self.cursor.close()
            self.conn.commit()
            self.conn.close()

            return existing is not None

        except mysql.connector.Error as err:
            print("Something went wrong: {}".format(err))
            abort(500)