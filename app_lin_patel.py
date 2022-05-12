from flask import Flask, render_template, request, redirect
from flask_mysqldb import MySQL

app = Flask(__name__)
app.config['MYSQL_HOST'] = 'classmysql.engr.oregonstate.edu'
app.config['MYSQL_USER'] = 'cs340_linhua'
app.config['MYSQL_PASSWORD'] = '6152' #last 4 of onid
app.config['MYSQL_DB'] = 'cs340_linhua'
app.config['MYSQL_CURSORCLASS'] = "DictCursor"


mysql = MySQL(app)


@app.route("/")
def hello_world():
    return render_template(
        'home.html',
        title="Home Page"
    )

@app.route("/customers")
def customers():
    return render_template(
        'entity.html',
        title="Customers",
        headers=["customer_id", "first_name", "last_name", "age", "email", "is_active", "street", "city", "state", "zip", "country", "phone"],
        data=[
            ["1","HuanChun","Lin","25","lin@gmail.com","0","1701 SW Western Blvd.","Corvallis","OR","97333","US","541.737.2464"],
            ["2","Satyam","Patel","27","patel@gmail.com","1","1600 Amphitheatre Parkway","Mountain View","CA","97333","US","209.513.0514"],
            ["3","Elon","Musk","35","musk@gmail.com","0","3500 Deer Creek Road","Corvallis","OR","97333","US","310.709.9497"]
        ],
        PageHeader="Customers Table",
        UpdateRoute="/update/customers", #TODO change this in the future to the actual route
        DeleteRoute="/customers", #TODO change this in the future to the actual route
        InsertRoute="/customers" #TODO change this in the future to the actual route
    )

@app.route("/houses")
def houses():

    search = request.args.get("search")

    query = "SELECT * FROM Houses;"
    if search is not None and search is not "":
        print(search)
        query = "SELECT * FROM Houses WHERE street = " + "'" + search + "'" + ";"


    cur = mysql.connection.cursor()
    cur.execute(query)
    results = cur.fetchall()
    data = list()
    for result in results:
        data.append(result.values())

    attributes = ["No houses found for that street"]
    if len(results) > 0:
        attributes = results[0].keys()
   
    return render_template(
        'entity.html',
        title="Houses",
        headers=attributes, 
        data=data,
        PageHeader="Houses Table",
        UpdateRoute="/update/houses", #TODO change this in the future to the actual route
        DeleteRoute="/houses", #TODO change this in the future to the actual route
        InsertRoute="/insert/houses", #TODO change this in the future to the actual route
        SearchRoute="/houses"
    )

@app.route("/sales")
def sales():
    return render_template(
        'entity.html',
        title="Sales",
        headers=["sale_id", "house_id", "customer_id", "date", "sale_price", "profit"],
        data=[
            ["1","1","1","2022-02-28","890000.0000","340000.0000"],
            ["2","2","2","2022-03-15","659800.0000","144000.0000"],
            ["3","3","3","2022-02-28","895200.0000","151200.0000"]
        ],
        PageHeader="Sales Table",
        UpdateRoute="/update/sales", #TODO change this in the future to the actual route
        DeleteRoute="/sales", #TODO change this in the future to the actual route
        InsertRoute="/sales" #TODO change this in the future to the actual route
    )

@app.route("/customer_house_wishes")
def wishes():
    return render_template(
        'entity.html',
        title="Customer House Wishes",
        headers=["wish_id", "house_id", "customer_id", "create_at", "updated_at"],
        data=[
            ["1","1","1","2022-05-02 01:00:00","2022-05-10 01:00:00"],
            ["2","1","2","2022-05-01 01:00:00","2022-05-11 01:00:00"],
            ["3","3","2","2022-05-01 01:00:00","2022-05-01 01:00:00"]
        ],
        PageHeader="Customer House Wishes",
        UpdateRoute="/update/customer_house_wishes", #TODO change this in the future to the actual route
        DeleteRoute="/customer_house_wishes", #TODO change this in the future to the actual route
        InsertRoute="/customer_house_wishes" #TODO change this in the future to the actual route
    )

@app.route("/categories")
def categories():
    return render_template(
        'entity.html',
        title="Categories",
        headers=["category_id", "name", "beds", "baths"],
        data=[
            ["1","single-family","3", "2"],
            ["2","condo","2", "2"],
            ["3","town house","4", "3"]
        ],
        PageHeader="Categories Table",
        UpdateRoute="/update/categories", #TODO change this in the future to the actual route
        DeleteRoute="/categories", #TODO change this in the future to the actual route
        InsertRoute="/categories" #TODO change this in the future to the actual route
    )
@app.route("/insert/houses",methods=["POST"])
def insert_houses():
    form_data =request.form
    category_id=form_data["category_id"]
    list_date=form_data["list_date"]
    list_price=form_data["list_price"]
    adjusted_price=form_data["adjusted_price"]
    street=form_data["street"]
    city=form_data["city"]
    state=form_data["state"]
    _zip=form_data["zip"]
    location_description=form_data["location_description"]

    
    query = "INSERT INTO Houses (category_id, list_date, list_price, adjusted_price, street, city, state, zip, location_description) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s);"
    cur = mysql.connection.cursor()
    cur.execute(query,(category_id, list_date, list_price, adjusted_price, street, city, state, _zip, location_description))
    mysql.connection.commit()
    return redirect("/houses")
@app.route("/update/customers")
def update_customers():
    return render_template(
        'update.html',
        attributes=["customer_id", "first_name", "last_name", "age", "email", "is_active", "street", "city", "state", "zip", "country", "phone"],
        UpdateRoute="/customers"
    )

@app.route("/update/houses")
def update_houses():
    return render_template(
        'update.html',
        attributes=["house_id", "category_id", "list_date", "list_price", "adjusted_price", "street", "city", "state", "zip", "location_description"],
        UpdateRoute="/houses"
    )

@app.route("/update/sales")
def update_sales():
    return render_template(
        'update.html',
        attributes=["sale_id", "house_id", "customer_id", "date", "sale_price", "profit"],
        UpdateRoute="/sales"
    )

@app.route("/update/customer_house_wishes")
def update_customer_house_wishes():
    return render_template(
        'update.html',
        attributes=["wish_id", "house_id", "customer_id", "create_at", "updated_at"],
        UpdateRoute="/customer_house_wishes"
    )

@app.route("/update/categories")
def update_categories():
    return render_template(
        'update.html',
        attributes=["category_id", "name", "description"],
        UpdateRoute="/categories"
    )
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8765, debug=True)