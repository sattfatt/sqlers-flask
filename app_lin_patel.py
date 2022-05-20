from flask import Flask, render_template, request, redirect, Request
from flask_mysqldb import MySQL
from database import SetupDatabaseConnection, RunSelectQuery, RunUpdateQuery, RunDeleteQuery, RunInsertQuery
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
    data, tableHeader = RunSelectQuery("Customers", mysql)
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

    where = None
    if search is not None and search != "":
        where = ("street", search)

    data, tableHeader = RunSelectQuery("Houses", mysql, where)

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
    data, tableHeader = RunSelectQuery("Sales", mysql)
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
    data, tableHeader = RunSelectQuery("Customer_House_Wishes", mysql)

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
    data, tableHeader = RunSelectQuery("Categories", mysql)

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
    RunInsertQuery("Customer_House_Wishes", request.form, mysql)
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
    return update_helper(request, "Houses", "house_id", "/houses")


@app.route("/update/sales", methods=["GET", "POST"])
def update_sales():
    return update_helper(request, "Sales", "sale_id", "/sales")


@app.route("/update/customer_house_wishes", methods=["GET", "POST"])
def update_customer_house_wishes():
    return update_helper(request, "Customer_House_Wishes", "wish_id", "/customer_house_wishes")


@app.route("/update/categories", methods=["GET", "POST"])
def update_categories():
    return update_helper(request, "Categories", "category_id", "/categories")


def update_helper(req, table, id_attribute, redirect_path):
    if req.method == "GET":
        query = "SELECT * FROM {} WHERE {}={}".format(
            table, id_attribute, req.args["id"])
        data, attributes = RunSelectQuery(query, mysql)
        zipped = list(zip(data[0], attributes))

        return render_template(
            'update.html',
            attributes=zipped,
            UpdateRoute="/update{}".format(redirect_path)
        )
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
