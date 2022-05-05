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
        'customers.html',
        title="Customers",
        headers=["customer_id", "first_name", "last_name", "age", "email", "is_active", "street", "city", "state", "zip", "country", "phone"],
        data=[
            [1,"bob", "patel", "13", "asdf@sadfa.com", "true", "asdf N street", "porterville", "california", "54453", "US", "123123211"],
            [1,"bob", "patel", "13", "asdf@sadfa.com", "true", "asdf N street", "porterville", "california", "54453", "US", "123123211"]
        ]
    )

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8765, debug=True)