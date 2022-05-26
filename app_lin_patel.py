from flask import Flask, render_template, request, redirect, Request
from flask_mysqldb import MySQL
from database import SetupDatabaseConnection, RunSelectQuery, RunUpdateQuery, RunDeleteQuery, RunInsertQuery, GetCategoryNames, Beautify, GetAttributes, GetHouseStreets, GetCustomerNames
from werkzeug.datastructures import ImmutableOrderedMultiDict

# -------------
#    SETUP
# -------------


class OverrideRequest(Request):
    parameter_storage_class = ImmutableOrderedMultiDict


class OverrideFlask(Flask):
    request_class = OverrideRequest


app = OverrideFlask(__name__)

SetupDatabaseConnection(app)

mysql = MySQL(app)

# -------------
#   RETRIEVE
# -------------


@app.route("/")
def hello_world():
    return render_template(
        'home.html',
        title="Home Page"
    )


@app.route("/customers")
def customers():
    data = RunSelectQuery("Customers", mysql)
    tableHeader = GetAttributes("Customers", mysql)
    labels = Beautify(tableHeader)
    return render_template(
        'entity.html',
        title="Customers",
        headers=tableHeader,
        data=data,
        labels=labels[1:],
        PageHeader="Customers Table",
        UpdateRoute="/update/customers",
        DeleteRoute="/delete/customers",
        InsertRoute="/insert/customers"
    )


@app.route("/houses")
def houses():

    data = RunSelectQuery("Houses", mysql, search_helper(request, "street"))
    tableHeader = GetAttributes("Houses", mysql)
    cat = GetCategoryNames(mysql)
    labels = Beautify(tableHeader)
    return render_template(
        'entity.html',
        title="Houses",
        headers=tableHeader,
        data=data,
        categories=cat,
        labels=labels[1:],
        PageHeader="Houses Table",
        UpdateRoute="/update/houses",
        DeleteRoute="/delete/houses",
        InsertRoute="/insert/houses",
        SearchRoute="/houses",
        SearchAttribute="street"
    )


@app.route("/sales")
def sales():
    data = RunSelectQuery("Sales", mysql)
    tableHeader = GetAttributes("Sales", mysql)
    customers = GetCustomerNames(mysql)
    houses = GetHouseStreets(mysql)
    labels = Beautify(tableHeader)
    return render_template(
        'entity.html',
        title="Sales",
        headers=tableHeader,
        data=data,
        labels=labels[1:],
        customers=customers,
        houses=houses,
        PageHeader="Sales Table",
        UpdateRoute="/update/sales",
        DeleteRoute="/delete/sales",
        InsertRoute="/insert/sales"
    )


@app.route("/customer_house_wishes")
def wishes():
    data = RunSelectQuery("Customer_House_Wishes", mysql)
    tableHeader = GetAttributes("Customer_House_Wishes", mysql)
    houses = GetHouseStreets(mysql)
    customers = GetCustomerNames(mysql)
    labels = Beautify(tableHeader)
    return render_template(
        'entity.html',
        title="Customer House Wishes",
        headers=tableHeader,
        data=data,
        labels=labels[1:],
        houses=houses,
        customers=customers,
        PageHeader="Customer House Wishes",
        UpdateRoute="/update/customer_house_wishes",
        DeleteRoute="/delete/customer_house_wishes",
        InsertRoute="/insert/customer_house_wishes"
    )


@app.route("/categories")
def categories():
    data = RunSelectQuery("Categories", mysql)
    tableHeader = GetAttributes("Categories", mysql)
    labels = Beautify(tableHeader)
    return render_template(
        'entity.html',
        title="Categories",
        headers=tableHeader,
        data=data,
        labels=labels[1:],
        PageHeader="Categories Table",
        UpdateRoute="/update/categories",
        DeleteRoute="/delete/categories",
        InsertRoute="/insert/categories",
    )

def search_helper(request, attribute_name):
    search = request.args.get("search")
    where = None
    if search is not None and search != "":
        where = (attribute_name, search)
    return where


# -------------
#    INSERT
# -------------


@app.route("/insert/customers", methods=["POST"])
def insert_customers():
    RunInsertQuery("Customers", request.form, mysql)
    return redirect("/customers")


@app.route("/insert/houses", methods=["POST"])
def insert_houses():
    RunInsertQuery("Houses", request.form, mysql)
    return redirect("/houses")


@app.route("/insert/sales", methods=["POST"])
def insert_sales():
    RunInsertQuery("Sales", request.form, mysql)
    return redirect("/sales")


@app.route("/insert/customer_house_wishes", methods=["POST"])
def insert_wishes():
    query = "INSERT INTO Customer_House_Wishes (house_id,customer_id,create_at,updated_at) VALUES (%s,%s,CURRENT_TIMESTAMP(),CURRENT_TIMESTAMP());"
    cur = mysql.connection.cursor()
    cur.execute(query, [request.form["house_id"], request.form["customer_id"]])
    mysql.connection.commit()
    return redirect("/customer_house_wishes")


@app.route("/insert/categories", methods=["POST"])
def insert_categories():
    RunInsertQuery("Categories", request.form, mysql)
    return redirect("/categories")

# -------------
#    UPDATE
# -------------


@app.route("/update/customers", methods=["GET", "POST"])
def update_customers():
    return update_helper(request, "Customers", "customer_id", "/customers")


@app.route("/update/houses", methods=["GET", "POST"])
def update_houses():
    cat = GetCategoryNames(mysql)
    return update_helper(request, "Houses", "house_id", "/houses", categories=cat)


@app.route("/update/sales", methods=["GET", "POST"])
def update_sales():
    houses = GetHouseStreets(mysql)
    return update_helper(request, "Sales", "sale_id", "/sales", houses=houses)


@app.route("/update/customer_house_wishes", methods=["GET", "POST"])
def update_customer_house_wishes():
    def query_func():
        query = "UPDATE Customer_House_Wishes SET house_id=%s,customer_id=%s,updated_at=CURRENT_TIMESTAMP() WHERE wish_id=%s;"
        cur = mysql.connection.cursor()
        cur.execute(query, [request.form["house_id"], request.form["customer_id"], request.form["wish_id"]])
        mysql.connection.commit()
    houses = GetHouseStreets(mysql)
    customers = GetCustomerNames(mysql)
    return update_helper(request, "Customer_House_Wishes", "wish_id", "/customer_house_wishes", query_func=query_func, houses=houses, customers=customers)


@app.route("/update/categories", methods=["GET", "POST"])
def update_categories():
    return update_helper(request, "Categories", "category_id", "/categories")


def update_helper(req, table, id_attribute, redirect_path, houses=None, customers=None, categories=None, query_func=None):
    if req.method == "GET":
        data = RunSelectQuery(table, mysql, (id_attribute, req.args["id"]))
        attributes = GetAttributes(table, mysql)
        labels = Beautify(attributes)
        zipped = list(zip(data[0], attributes))
        return render_template(
            'update.html',
            attributes=zipped,
            UpdateRoute="/update{}".format(redirect_path),
            houses=houses,
            customers=customers,
            categories=categories,
            labels=labels
        )
    else:
        if query_func:
            query_func()
        else:
            args = req.form
            RunUpdateQuery(table, args, mysql)
        return redirect(redirect_path)

# -------------
#    DELETE
# -------------


@app.route("/delete/customers",)
def delete_customers():
    RunDeleteQuery("Customers", request.args, "customer_id", mysql)
    return redirect("/customers")


@app.route("/delete/houses",)
def delete_houses():
    RunDeleteQuery("Houses", request.args, "house_id", mysql)
    return redirect("/houses")


@app.route("/delete/categories",)
def delete_categories():
    RunDeleteQuery("Categories", request.args, "category_id", mysql)
    return redirect("/categories")


@app.route("/delete/customer_house_wishes",)
def delete_customer_house_wishes():
    RunDeleteQuery("Customer_House_Wishes", request.args, "wish_id", mysql)
    return redirect("/customer_house_wishes")


@app.route("/delete/sales",)
def delete_sales():
    RunDeleteQuery("Sales", request.args, "sale_id", mysql)
    return redirect("/sales")

# -------------
#    MAIN
# -------------


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8765, debug=True)
