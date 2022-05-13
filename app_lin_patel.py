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
        UpdateRoute="/update/customers",
        DeleteRoute="/delete/customers",
        InsertRoute="/insert/customers"
    )

@app.route("/houses")
def houses():

    search = request.args.get("search")

    query = "SELECT * FROM Houses;"
    if search is not None and search != "":
        print(search)
        query = "SELECT * FROM Houses WHERE street = '{}';".format(search)

    data, tableHeader = RunSelectQuery(query, mysql)

    return render_template(
        'entity.html',
        title="Houses",
        headers=tableHeader, 
        data=data,
        PageHeader="Houses Table",
        UpdateRoute="/update/houses",
        DeleteRoute="/delete/houses",
        InsertRoute="/insert/houses",
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
        UpdateRoute="/update/sales",
        DeleteRoute="/delete/sales",
        InsertRoute="/insert/sales"
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
        UpdateRoute="/update/customer_house_wishes",
        DeleteRoute="/delete/customer_house_wishes",
        InsertRoute="/insert/customer_house_wishes"
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
        UpdateRoute="/update/categories",
        DeleteRoute="/delete/categories",
        InsertRoute="/insert/categories"
    )

@app.route("/insert/customers",methods=["POST"])
def insert_customers():
    form_data =request.form
    first_name=form_data["first_name"]
    last_name=form_data["last_name"]
    age=form_data["age"]
    email=form_data["email"]
    is_active=form_data["is_active"]
    street=form_data["street"]
    city=form_data["city"]
    state=form_data["state"]
    _zip=form_data["zip"]
    country=form_data["country"]
    phone=form_data["phone"]

    query = "INSERT INTO Customers (first_name, last_name, age, email, is_active, street, city, state, zip, country, phone) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);"
    cur = mysql.connection.cursor()
    cur.execute(query,(first_name, last_name, age, email, is_active, street, city, state, _zip, country, phone))
    mysql.connection.commit()
    return redirect("/customers")

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

@app.route("/insert/sales",methods=["POST"])
def insert_sales():
    form_data =request.form
    house_id=form_data["house_id"]
    customer_id=form_data["customer_id"]
    date=form_data["date"]
    sale_price=form_data["sale_price"]
    profit=form_data["profit"]

    query = "INSERT INTO Sales (house_id, customer_id, date, sale_price, profit) VALUES (%s,%s,%s,%s,%s);"
    cur = mysql.connection.cursor()
    cur.execute(query,(house_id, customer_id, date, sale_price, profit))
    mysql.connection.commit()
    return redirect("/sales")

@app.route("/insert/customer_house_wishes",methods=["POST"])
def insert_wishes():
    form_data =request.form
    house_id=form_data["house_id"]
    customer_id=form_data["customer_id"]
    create_at=form_data["create_at"]
    updated_at=form_data["updated_at"]

    query = "INSERT INTO Customer_House_Wishes (house_id, customer_id, create_at, updated_at) VALUES (%s,%s,%s,%s);"
    cur = mysql.connection.cursor()
    cur.execute(query,(house_id, customer_id, create_at, updated_at))
    mysql.connection.commit()
    return redirect("/customer_house_wishes")

@app.route("/insert/categories",methods=["POST"])
def insert_categories():
    form_data =request.form
    name=form_data["name"]
    rooms=form_data["rooms"]
    baths=form_data["baths"]

    query = "INSERT INTO Categories (name, rooms, baths) VALUES (%s,%s,%s);"
    cur = mysql.connection.cursor()
    cur.execute(query,(name, rooms, baths))
    mysql.connection.commit()
    return redirect("/categories")

@app.route("/delete/categories",)
def delete_categories():
    form_data =request.form
    name=form_data["name"]
    rooms=form_data["rooms"]
    baths=form_data["baths"]

    query = "DELETE FROM Categories"
    cur = mysql.connection.cursor()
    cur.execute(query,(name, rooms, baths))
    mysql.connection.commit()
    return redirect("/categories")

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