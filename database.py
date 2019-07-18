import os
import pyodbc
import sys
from contextlib import contextmanager

server = os.environ['dbUrl']
database = os.environ['db']
username = os.environ['dbUser']
password = os.environ['dbUserPassword']
driver = '{ODBC Driver 17 for SQL Server}'
connection_str = 'DRIVER=' + driver + ';SERVER=' + server + \
                 ';PORT=1433;DATABASE=' + database + ';UID=' + username + ';PWD=' + password


@contextmanager
def open_db_connection(commit=False):
    connection = pyodbc.connect(connection_str)
    cursor = connection.cursor()
    try:
        yield cursor
    except pyodbc.DatabaseError as err:
        error = err.args[1]
        sys.stderr.write(error)
        cursor.execute("ROLLBACK")
        raise err
    else:
        if commit:
            cursor.execute("COMMIT")
        else:
            cursor.execute("ROLLBACK")
    finally:
        connection.close()
