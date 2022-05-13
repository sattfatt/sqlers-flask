def SetupDatabaseConnection(app):
    app.config['MYSQL_HOST'] = 'classmysql.engr.oregonstate.edu'
    app.config['MYSQL_USER'] = 'cs340_linhua'
    app.config['MYSQL_PASSWORD'] = '6152' #last 4 of onid
    app.config['MYSQL_DB'] = 'cs340_linhua'
    app.config['MYSQL_CURSORCLASS'] = "DictCursor"


def RunSelectQuery(query, mysql):
    cur = mysql.connection.cursor()
    cur.execute(query)
    results = cur.fetchall()
    data = [result.values() for result in results]
    keys = []
    if len(results) > 0:
        keys = list(results[0].keys())

    return data, keys

def RunInsertQuery(query, data, mysql):
    pass