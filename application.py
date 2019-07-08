from flask import Flask, request
import json

app = Flask(__name__)


@app.route("/api/signup", methods=['POST'])
def signup_mock():
    return json.dumps({
        "name": "rahul",
        "number": "7897580575"
    })


@app.route("/api/contacts", methods=['POST', 'GET'])
def contacts_mock():
    requestJson = request.json;
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
    return "Hello World!"

def connectDB():
    import pyodbc
    cnxn = pyodbc.connect('sqlserver://finderdb.database.windows.net:1433;database=finderdb;user=rax@finderdb;password=;Px{B?c}NFz3]JM5;encrypt=true;trustServerCertificate=false;hostNameInCertificate=*.database.windows.net;loginTimeout=30;')



if __name__ == "__main__":
    connectDB()
    app.run()
