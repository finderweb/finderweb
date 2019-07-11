import os
import pyodbc
import sys

dbUrl = os.environ['dbUrl']
# 'sqlserver://finderdb.database.windows.net'
db = os.environ['db']
# 'finderdb'
dbUser = os.environ['dbUser']
# 'rax@finderdb'
dbUserPassword = os.environ['dbUserPassword']
connection_string = dbUrl + ':1433;database=' \
                    + db + ';user=' \
                    + dbUser + ';password=;' \
                    + dbUserPassword + ';encrypt=true;' \
                                       'trustServerCertificate=false;' \
                                       'hostNameInCertificate=*.database.windows.net;loginTimeout=30;'


def init_db():
    connection = pyodbc.connect(dbUrl
                                + ':1433;database='
                                + db + ';user='
                                + dbUser + ';password=;'
                                + dbUserPassword + ';encrypt=true;'
                                                   'trustServerCertificate=false;'
                                                   'hostNameInCertificate=*.database.windows.net;loginTimeout=30;')
    return connection


def storeContacts():
    pass


def readContacts():
    pass


def open_db_connection(commit=False):
    connection = pyodbc.connect(connection_string)
    cursor = connection.cursor()
    try:
        yield cursor
    except pyodbc.DatabaseError as err:
        error, = err.args
        sys.stderr.write(error.message)
        cursor.execute("ROLLBACK")
        raise err
    else:
        if commit:
            cursor.execute("COMMIT")
        else:
            cursor.execute("ROLLBACK")
    finally:
        connection.close()
#
# if __name__ == "__main__":
#     initDb()

# Once the value are read, I will start doing somethint
