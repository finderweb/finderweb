from database import open_db_connection
import os
import datetime

db = os.environ['db']
account_name = os.environ['accountName']
account_key = os.environ['accountKey']
userNode = db + '.dbo.' + 'UserNode'


def is_user_present(number):
    number = trim_number(number)
    with open_db_connection() as cursor:
        cursor.execute('select user_id,name,number,self_signed from finderdb.dbo.UserNode where number like ?', number)
        row = cursor.fetchone()
        if row is None:
            return False, None
        return True, {
            'userId': row.user_id,
            'name': row.name,
            'number': row.number,
            'selfSigned': row.self_signed
        }


def has_user_signup(number):
    number = trim_number(number)
    is_present, user = is_user_present(number)
    if not is_present:
        return {"number": number, "signedUp": False}
    if user["selfSigned"]:
        return {"number": number, "signedUp": True}
    return {"number": number, "signedUp": False}


def create_insert_node_query(name, number):
    name = trim_name(name)
    if len(name) > 240 or len(number) > 20 or len(number) < 10:
        return ""
    return " IF not EXISTS( Select * from UserNode where number like '" + number + "') BEGIN insert into UserNode(name, number, self_signed) values('" + name + "','" + number + "', 0) END \n"


def convert_to_utf8(number):
    utf = ""
    for ch in number:
        if ch == '0' or ch == '1' or ch == '2' or ch == '3' or ch == '4' or ch == '5' or ch == '6' or ch == '7' or ch == '8' or ch == '9':
            utf = utf + ch
    return utf


def trim_number(number):
    number = convert_to_utf8(number)
    number = number.strip()
    if len(number) == 0 or len(number) < 10:
        return number
    if number[0] == '9' and number[1] == '1':
        return number[2::]
    if number[0] == '0':
        return number[1:]
    return number


def trim_name(name):
    fname = ""
    for ch in name:
        if 'a' <= ch <= 'z':
            fname += ch
        elif 'A' <= ch <= 'Z':
            fname += ch
        else:
            fname += ' '
    return fname


def insert_contacts(user, contacts):
    user["number"] = trim_number(user["number"])
    nodes_query = ""
    edges_query = ""
    for contact in contacts:
        nodes_query += create_insert_node_query(trim_name(contact["name"]), trim_number(contact["number"]))
    for contact in contacts:
        edges_query += create_insert_edge_query(user, trim_name(contact["name"]), contact["number"])
    execute_query(nodes_query)
    execute_query(edges_query)


def create_insert_edge_query(user, name, destination_number):
    destination_number = trim_number(destination_number)
    source_number = trim_number(user["number"])
    if len(destination_number) > 20 or len(source_number) > 20 or len(destination_number) < 10 or len(source_number) < 10:
        return ""
    return " IF not EXISTS ( select * from knowsEdge where source_destination like '" + source_number + destination_number + "') BEGIN insert into knowsEdge values((select $node_id from userNode where number like'" + source_number + "'),(select $node_id from userNode where number like '" + destination_number + "'),'" + name + "','" + source_number + destination_number + "') END \n"


def execute_query(query):
    with open_db_connection(True) as cursor:
        cursor.execute(query)


def insert_user_util(name, number, self_signed):
    with open_db_connection(True) as cursor:
        cursor.execute('insert into finderdb.dbo.userNode(name,number,self_signed) values(?,?,?)', name, number,
                       self_signed)


# There will be a case where there are new contacts added,
def signup_user(number, name, self_signed=True):
    number = trim_number(number)
    if len(number) != 10:
        raise Exception("Phone Number must have length equal to 10")
    is_present, user = is_user_present(number)
    if not is_present:
        with open_db_connection(True) as cursor:
            cursor.execute(
                'insert into finderdb.dbo.userNode(name,number,self_signed,contacts_synced,created_on, modified_on) '
                'values(?,?,?,?,?,?)', name, number, self_signed, 0, datetime.datetime.now(), datetime.datetime.now())
    else:
        if not user["selfSigned"]:
            with open_db_connection(True) as cursor:
                cursor.execute("update finderdb.dbo.userNode set self_signed=1 , name = ? where number like ?", name,
                               number)
    return {"number": number, "name": name, "selfSigned": True}
    # return is_user_present(number)


def search_mutual(source_number, destination_number, length=1):
    source_number = trim_number(source_number)
    destination_number = trim_number(destination_number)
    results = []
    if length == 1:
        results = results + get_common_contacts_of_length_1(source_number, destination_number)
    if length == 2:
        results = results + get_common_contacts_of_length_2(source_number, destination_number)
    if len(results) == 0:
        results = [{
            "sourceNumber": source_number,
            "destinationNumber": destination_number,
            "edges": []
        }]
    return {"results": results}


def get_result_object(source_number, destination_number, edges):
    result = {"sourceNumber": source_number, "destinationNumber": destination_number, "edges": edges}
    return result


def get_edges(node_number, contact_name, order):
    return {
        "nodeNumber": node_number,
        "contactName": contact_name,
        "order": order
    }


def get_common_contacts(source_number, destination_number):
    results = list()
    results.append(get_common_contacts_of_length_1(source_number, destination_number))
    results.append(get_common_contacts_of_length_2(source_number, destination_number))
    return results


def get_common_contacts_of_length_1(source_number, destination_number):
    results = []
    with open_db_connection() as cursor:
        cursor.execute("select node2.number as number, node2.name as name from UserNode node1, knowsEdge edge1, "
                       "knowsEdge edge2, UserNode node2, UserNode node3 Where match(node1-(edge1)->node2-("
                       "edge2)->node3) and node1.number like ? and node3.number like ?"
                       , source_number, destination_number)
        rows = cursor.fetchall()
        for row in rows:
            edges = list()
            # edges.append(get_edges(source_number, source_number, 0))
            edges.append(get_edges(row.number, row.name, 1))
            # edges.append(get_edges(destination_number, destination_number, 2))
            results.append(get_result_object(source_number, destination_number, edges))
    return results


def get_common_contacts_of_length_2(source_number, destination_number):
    results = []
    with open_db_connection() as cursor:
        cursor.execute("select node2.number as number1, node2.name as name1, node3.number as number2, node3.name as "
                       "name2 as name from UserNode node1, knowsEdge edge1,knowsEdge edge2,knowsEdge edge3, UserNode "
                       "node2, UserNode node3, UserNode node4 Where match(node1-(edge1)->node2-("
                       "edge2)->node3-(edge3)->node4) and node1.number like ? and node4.number like ?"
                       , source_number, destination_number)
        rows = cursor.fetchall()
        for row in rows:
            edges = list()
            # edges.append(get_edges(source_number, source_number, 0))
            edges.append(get_edges(row.number1, row.name1, 1))
            edges.append(get_edges(row.numer2, row.name2, 2))
            # edges.append(get_edges(destination_number, destination_number, 3))
            results.append(get_result_object(source_number, destination_number, edges))
    return results
