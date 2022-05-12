from flask import Flask, render_template, request, redirect
from flask_mysqldb import MySQL
from database import SetupDatabaseConnection, RunSelectQuery

app = Flask(__name__)

SetupDatabaseConnection(app)

mysql = MySQL(app)

@app.route("/")
def hello_world():
    return render_template(
        'home.html',
        title="Home Page"
    )

@app.route("/customers")
def customers():
    query = "SELECT * FROM Customers;"
    data, tableHeader = RunSelectQuery(query, mysql)
    return render_template(
        'entity.html',
        title="Customers",
        headers=tableHeader,
        data=data,
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
        query = "SELECT * FROM Houses WHERE street = '{}';".format(search)

    data, tableHeader = RunSelectQuery(query, mysql)

    return render_template(
        'entity.html',
        title="Houses",
        headers=tableHeader, 
        data=data,
        PageHeader="Houses Table",
        UpdateRoute="/update/houses", #TODO change this in the future to the actual route
        DeleteRoute="/houses", #TODO change this in the future to the actual route
        InsertRoute="/insert/houses", #TODO change this in the future to the actual route
        SearchRoute="/houses"
    )

@app.route("/sales")
def sales():
    query = "SELECT * FROM Sales;"
    data, tableHeader = RunSelectQuery(query, mysql)
    return render_template(
        'entity.html',
        title="Sales",
        headers=tableHeader,
        data=data,
        PageHeader="Sales Table",
        UpdateRoute="/update/sales", #TODO change this in the future to the actual route
        DeleteRoute="/sales", #TODO change this in the future to the actual route
        InsertRoute="/sales" #TODO change this in the future to the actual route
    )

@app.route("/customer_house_wishes")
def wishes():
    query = "SELECT * FROM Customer_House_Wishes;"
    data, tableHeader = RunSelectQuery(query, mysql)
    
    return render_template(
        'entity.html',
        title="Customer House Wishes",
        headers=tableHeader,
        data=data,
        PageHeader="Customer House Wishes",
        UpdateRoute="/update/customer_house_wishes", #TODO change this in the future to the actual route
        DeleteRoute="/customer_house_wishes", #TODO change this in the future to the actual route
        InsertRoute="/customer_house_wishes" #TODO change this in the future to the actual route
    )

@app.route("/categories")
def categories():

    query = "SELECT * FROM Categories;"
    data, tableHeader = RunSelectQuery(query, mysql)
    
    return render_template(
        'entity.html',
        title="Categories",
        headers=tableHeader,
        data=data,
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