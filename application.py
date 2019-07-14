from flask import Flask, request
import json

from user import insert_user, insert_contacts, search_mutual, has_user_signup

app = Flask(__name__)


def throw_error(code, success, message):
    return json.dumps({
        code: code,
        success: success,
        message: message
    })


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
    return return_json(insert_user(name=name, number=number))


@app.route("/api/contacts", methods=['POST', 'GET'])
def contacts():
    request_json = request.json
    if "user" not in request_json or request_json["user"] is None:
        return throw_error(-1, False, "User is not present")
    if "contacts" not in request_json or request_json["contacts"] is None:
        return throw_error(-1, False, "Contacts are not present")
    user = request_json["user"]
    name, number = user["name"], user["number"]
    if number is None:
        return throw_error(-1, False, "Number is not present")
    contactslist = request_json["contacts"]
    if contactslist is None:
        return throw_error(-1, False, "Contact list is empty")
    return json.dumps(insert_contacts(user, contactslist))


@app.route("/api/search", methods=['GET'])
def search_mock():
    source_number = request.args.get('source')
    destination_number = request.args.get('destination')
    if source_number is None or destination_number is None:
        return throw_error(-1, False, "Source or Destination number not mentioned")
    return json.dumps(search_mutual(source_number, destination_number))


@app.route("/")
def hello():
    return "Hello There!!"


@app.route("/api/signup", methods=['GET'])
def user_signup():
    number = request.args.get('number')
    if number is None or len(number) != 10:
        throw_error(-1, False, "Number can not be empty")
    return json.dumps(has_user_signup(number))


if __name__ == "__main__":
    app.run()
