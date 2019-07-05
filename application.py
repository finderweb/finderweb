from flask import Flask

app = Flask(__name__)


@app.route("/api/signup")
def signup_mock():
    return {
        "name": "rahul",
        "number": "7897580575"
    }


@app.route("/api/contacts")
def contacts_mock():
    return {
        "name": "rahul",
        "number": "7897580575"
    }


@app.route("/api/search")
def search_mock():
    return {
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
    }


@app.route("/")
def hello():
    return "Hello World!"
