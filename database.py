import os
import pyodbc

dbUrl = os.environ['dbUrl']
# 'sqlserver://finderdb.database.windows.net'
db = os.environ['db']
# 'finderdb'
dbUser = os.environ['dbUser']
# 'rax@finderdb'
dbUserPassword = os.environ['dbUserPassword']


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
#
# if __name__ == "__main__":
#     initDb()

# Once the value are read, I will start doing somethint
