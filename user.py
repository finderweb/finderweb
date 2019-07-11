from database import open_db_connection
import os

db = os.environ['db']


def is_user_present(phone):
    with open_db_connection() as cursor:
        cursor.execute('select * from ' + db + '.dbo.' + 'UserNode')
        for row in cursor:
            print(row)
            return row


def insert_user(number, name, database, force=False):
    random_id = ""
    return {
        "name": name,
        "number": number,
        "id": random_id
    }
