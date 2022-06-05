from typing import Tuple


def SetupDatabaseConnection(app):
    app.config['MYSQL_HOST'] = 'classmysql.engr.oregonstate.edu'
    app.config['MYSQL_USER'] = 'cs340_linhua'
    app.config['MYSQL_PASSWORD'] = '6152' #last 4 of onid
    app.config['MYSQL_DB'] = 'cs340_linhua'
    app.config['MYSQL_CURSORCLASS'] = "DictCursor"

def RunSearchQuery(table, mysql, search):
    print(search)

    all = "SELECT * FROM {};".format(table)

    query = "SELECT * FROM {} WHERE MATCH(street) AGAINST('{}*' IN BOOLEAN MODE );".format(table, search)

    if search == "" or search is None:
        query = all
    print(query)
    cur = mysql.connection.cursor()
    try:
        cur.execute(query)
    except:
        cur.execute(all)
        Dberror.seterror("Search using alpha numerics only please!")
    results = cur.fetchall()
    data = [list(result.values()) for result in results]
    return data


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

    return data


def RunInsertQuery(table, form, mysql):
    keys = list(form.keys())
    values = form.values()
    values = [None if value=="" else value for value in values]

    placeholder = ",".join(["%s" for value in values])

    query = "INSERT INTO {} ({}) VALUES ({});".format(table, ",".join(keys), placeholder)
    print(query)
    cur = mysql.connection.cursor()

    try:
        cur.execute(query, values)
    except:
        if table == "Sales":
            Dberror.seterror("could not insert into {}. House is already sold to someone! Or there are no houses left!".format(table))
        else:
            Dberror.seterror("could not insert into {}".format(table))

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
    print(query)

    cur = mysql.connection.cursor()
    try:
        cur.execute(query, values[1:])
    except:
        if table == "Sales":
            Dberror.seterror("could not update {} in {}. House is already sold to someone!".format(args, table))
        else:
            Dberror.seterror("could not update {} in {}".format(args, table))
    mysql.connection.commit()


def RunDeleteQuery(table, args, id_attribute, mysql):
    keys = list(args.keys())
    values = list(args.values())
    query = "DELETE FROM {} WHERE {}='{}';".format(table, id_attribute, values[0])
    cur = mysql.connection.cursor()
    cur.execute(query)
    mysql.connection.commit()


def GetAttributes(Table, mysql):
    query = "DESCRIBE {}".format(Table)
    cur = mysql.connection.cursor()
    cur.execute(query)
    result = cur.fetchall()
    result = [res['Field'] for res in result]
    print(result)
    return result


def GetHouseStreets(mysql):
    data = RunSelectQuery("Houses", mysql)
    houses = []
    for row in data:
        houses.append((row[0], row[5]))
    return houses


def GetCategoryNames(mysql):
    data = RunSelectQuery("Categories", mysql)
    categories = []
    for row in data:
        categories.append((row[0], row[1]))
    return categories

def GetCustomerNames(mysql):
    data = RunSelectQuery("Customers", mysql)
    customers = []
    for row in data:
        customers.append((row[0], " ".join((row[1], row[2]))))
    return customers

def Beautify(header):
    """Returns the headers in a more readable form."""
    newheader = [(" ".join(h.split("_"))).title() for h in header]
    return newheader


class Dberror:
    LastError = None
    @classmethod
    def seterror(cls, error):
        Dberror.LastError = error

    @classmethod
    def clearerror(cls):
        temp = Dberror.LastError
        Dberror.LastError = None
        return temp
