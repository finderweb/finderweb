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
    return requestJson
    # return json.dumps({
    #     "name": "rahul",
    #     # "number": "7897580575"
    # })


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


if __name__ == "__main__":
    app.run()
