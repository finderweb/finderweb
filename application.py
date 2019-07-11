from flask import Flask, request
import json

from database import init_db
from user import is_user_present, insert_user

db_connection = None
app = Flask(__name__)


def throw_error(code, success, message):
    return json.dumps({
        code: code,
        success: success,
        message: message
    })


def is_key_present():
    pass


def return_json(mp):
    return json.dumps(mp)


@app.route("/api/signup", methods=['POST'])
def signup():
    request_json = request.json

    if "name" not in request_json or request_json["name"] is None:
        return throw_error(-1, False, "Name is None")
    else:
        name = request_json["name"]

    if "number" not in request_json or request_json["number"] is None:
        return throw_error(-1, False, "Phone Number is None")
    else:
        number = request_json["number"]

    return return_json(insert_user(name=name, number=number, database=db_connection))


@app.route("/api/contacts", methods=['POST', 'GET'])
def contacts():
    requestJson = request.json
    return json.dumps(requestJson)


@app.route("/api/search")
def search_mock():
    return json.dumps({
        "sourceNumber": "07897580575",
        "sourceName": "Rahul",
        "destinationNumber": "09210022557",
        "destinationName": "Papa",
        "edges": [
            {
                "nodeNumber": "07897580575",
                "contactName": "Rahul",
                "order": 0
            },
            {
                "nodeNumber": "07897580575",
                "contactName": "Rahul Bansal",
                "order": 1
            },
            {
                "nodeNumber": "07897580575",
                "contactName": "Rahul 2",
                "order": 3
            },
            {
                "nodeNumber": "0897580575",
                "contactName": "Rahul 3",
                "order": 2
            }
        ]
    })


@app.route("/")
def hello():
    return is_user_present()
    # return "Hello World!"


# def connectDB():
    # import pyodbc
    # cnxn = pyodbc.connect('sqlserver://finderdb.database.windows.net:1433;database=finderdb;user=rax@finderdb;password=;;encrypt=true;trustServerCertificate=false;hostNameInCertificate=*.database.windows.net;loginTimeout=30;')
    # return cnxn

if __name__ == "__main__":
    db_connection = init_db()
    is_user_present()
    app.run()
