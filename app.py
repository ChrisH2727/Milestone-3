import os
from flask import (
    Flask, flash, render_template,
    redirect, request, session, url_for)
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
if os.path.exists("env.py"):
    import env


app = Flask(__name__)

app.config["MONGO_DBNAME"] = os.environ.get("MONGO_DBNAME")
app.config["MONGO_URI"] = os.environ.get("MONGO_URI")
app.secret_key = os.environ.get("SECRET_KEY")

mongo = PyMongo(app)

@app.route("/")

@app.route("/login")
def login():
    return render_template("login.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        # check if username already exists in db
        existing_user = mongo.db.users.find_one(
            {"first": request.form.get("first_name").lower()})
        print(existing_user)

        if existing_user:
            flash("Username already exists")
            print("exiting user")
            return redirect(url_for("register.html"))

        register = {
            "first": request.form.get("first_name").lower()
        }
        mongo.db.users.insert_one(register)

        flash("Registration Successful!")
        return redirect(url_for("login.html"))

    return render_template("register.html")










@app.route("/source_request")
def source_request():
    return render_template("sourceRequest.html")


@app.route("/usage_report")
def usage_report():
    return render_template("usageReport.html")


@app.route("/approve_request")
def approve_request():
    return render_template("approveRequest.html")


@app.route("/user_rights")
def user_rights():
    return render_template("user.html")


@app.route("/add_source")
def add_source():
    return render_template("addSource.html")


@app.route("/delete_source")
def delete_source():
    return render_template("deleteSource.html")


@app.route("/update_source")
def update_source():
    return render_template("updateSource.html")


@app.route("/get_sources")
def get_sources():
    sources = mongo.db.sources.find()
    return render_template("inventory.html", sources=sources)


if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
            port=int(os.environ.get("PORT")),
            debug=True)