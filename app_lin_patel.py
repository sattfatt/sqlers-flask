from flask import Flask
from flask import render_template

app = Flask(__name__)

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
        UpdateRoute="/customers", #TODO change this in the future to the actual route
        DeleteRoute="/customers", #TODO change this in the future to the actual route
        InsertRoute="/customers" #TODO change this in the future to the actual route
    )

@app.route("/houses")
def houses():
    return render_template(
        'entity.html',
        title="Houses",
        headers=["house_id", "category_id", "list_date", "list_price", "adjusted_price", "street", "city", "state", "zip", "location_description"],
        data=[
            ["3","","2022-01-01","842000.0000","895200.0000","1400 Bowe Ave","Santa Clara","CA","95051","Amazing Place! WOW!"],
            ["1","1","2022-01-02","848000.0000","890000.0000","144 3rd street","San Jose","CA","95112","Great Place! WOW!"],
            ["2","2","2022-03-02","649800.0000","659800.0000","255 Llano De Los Robles Ave","San Jose","CA","95136","Wonderful Place! WOW!"]
        ],
        PageHeader="Houses Table",
        UpdateRoute="/houses", #TODO change this in the future to the actual route
        DeleteRoute="/houses", #TODO change this in the future to the actual route
        InsertRoute="/houses" #TODO change this in the future to the actual route
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
        UpdateRoute="/sales", #TODO change this in the future to the actual route
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
        UpdateRoute="/customer_house_wishes", #TODO change this in the future to the actual route
        DeleteRoute="/customer_house_wishes", #TODO change this in the future to the actual route
        InsertRoute="/customer_house_wishes" #TODO change this in the future to the actual route
    )

@app.route("/categories")
def categories():
    return render_template(
        'entity.html',
        title="Categories",
        headers=["category_id", "name", "description"],
        data=[
            ["1","single-family","3bd 2ba"],
            ["2","condo","2bd 2ba"],
            ["3","town house","4bd 3ba"]
        ],
        PageHeader="Categories Table",
        UpdateRoute="/categories", #TODO change this in the future to the actual route
        DeleteRoute="/categories", #TODO change this in the future to the actual route
        InsertRoute="/categories" #TODO change this in the future to the actual route
    )
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8765, debug=True)