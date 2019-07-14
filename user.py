from database import open_db_connection
import os

db = os.environ['db']
userNode = db + '.dbo.' + 'UserNode'


def is_user_present(number):
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
    is_present, user = is_user_present(number)
    if not is_present:
        return {"number": number, "signedUp": False}
    if user["selfSigned"]:
        return {"number": number, "signedUp": True}
    return {"number": number, "signedUp": False}


def insert_contacts(user, contacts):
    for contact in contacts:
        insert_edge(user, contact)
    return None


def insert_edge(user, contact):
    upsert(contact)
    with open_db_connection(True) as cursor:
        cursor.execute("INSERT INTO finderdb.dbo.knowsEdge VALUES ((SELECT $node_id FROM finderdb.dbo.userNode WHERE "
                       "number = ?), (SELECT $node_id FROM finderdb.dbo.userNode WHERE number = ?),?);",
                       user["number"], contact["number"], contact["name"])


def upsert(contact):
    is_present, user = is_user_present(contact["number"])
    if not is_present:
        insert_user_util(contact["number"], contact["name"], self_signed=False)


def insert_user_util(name, number, self_signed):
    with open_db_connection(True) as cursor:
        cursor.execute('insert into finderdb.dbo.userNode(name,number,self_signed) values(?,?,?)', name, number,
                       self_signed)


def insert_user(number, name, self_signed=True):
    if len(number) != 10:
        raise Exception("Phone Number must have length equal to 10")
    is_present, user = is_user_present(number)
    if not is_present:
        with open_db_connection(True) as cursor:
            cursor.execute('insert into finderdb.dbo.userNode(name,number,self_signed) values(?,?,?)', name, number,
                           self_signed)
    else:
        if not user["selfSigned"]:
            with open_db_connection(True) as cursor:
                cursor.execute("update finderdb.dbo.userNode set self_singed=1 and name = ? where number like ?", name,
                               number)
    return {"number": number, "name": name, "selfSigned": True}
    # return is_user_present(number)


def search_mutual(source_number, destination_number, length=1):
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
    return results


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
            edges.append(get_edges(source_number, source_number, 0))
            edges.append(get_edges(row.number, row.name, 1))
            edges.append(get_edges(destination_number, destination_number, 2))
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
            edges.append(get_edges(source_number, source_number, 0))
            edges.append(get_edges(row.number1, row.name1, 1))
            edges.append(get_edges(row.numer2, row.name2, 2))
            edges.append(get_edges(destination_number, destination_number, 3))
            results.append(get_result_object(source_number, destination_number, edges))
    return results
