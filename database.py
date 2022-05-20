from typing import Tuple


def SetupDatabaseConnection(app):
    app.config['MYSQL_HOST'] = 'classmysql.engr.oregonstate.edu'
    app.config['MYSQL_USER'] = 'cs340_linhua'
    app.config['MYSQL_PASSWORD'] = '6152' #last 4 of onid
    app.config['MYSQL_DB'] = 'cs340_linhua'
    app.config['MYSQL_CURSORCLASS'] = "DictCursor"


def RunSelectQuery(table, mysql, where=None):
    query = "SELECT * FROM {};".format(table)
    if (where is not None):
        query = "SELECT * FROM {} WHERE {}='{}'".format(table, where[0], where[1])
    cur = mysql.connection.cursor()
    cur.execute(query)
    results = cur.fetchall()
    data = [list(result.values()) for result in results]
    keys = []
    if len(results) > 0:
        keys = list(results[0].keys())

    return data, keys

def RunInsertQuery(table, form, mysql):
    keys = list(form.keys())
    values = form.values()
    values = [None if value=="" else value for value in values]

    placeholder = ",".join(["%s" for value in values])

    query = "INSERT INTO {} ({}) VALUES ({});".format(table, ",".join(keys), placeholder)
    print(query)
    cur = mysql.connection.cursor()
    cur.execute(query, values)
    mysql.connection.commit()

def RunUpdateQuery(table, args, mysql):
    keys = list(args.keys())
    values = args.values()
    values = [None if value=="" else value for value in values]
    q = ""
    for key in keys[1:]:
        q += "{}=%s,".format(key)
    q = q[:-1]

    query = "UPDATE {} SET {} WHERE {}='{}';".format(table, q, keys[0], values[0])

    cur = mysql.connection.cursor()
    cur.execute(query, values[1:])
    mysql.connection.commit()

def RunDeleteQuery(table, args, id_attribute, mysql):
    keys = list(args.keys())
    values = list(args.values())
    query = "DELETE FROM {} WHERE {}='{}';".format(table, id_attribute, values[0])
    cur = mysql.connection.cursor()
    cur.execute(query)
    mysql.connection.commit()
    
