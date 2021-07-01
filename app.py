import os
from flask import (
    Flask, flash, render_template,
    redirect, request, session, url_for)
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from werkzeug.security import generate_password_hash, check_password_hash
if os.path.exists("env.py"):
    import env


app = Flask(__name__)

app.config["MONGO_DBNAME"] = os.environ.get("MONGO_DBNAME")
app.config["MONGO_URI"] = os.environ.get("MONGO_URI")
app.secret_key = os.environ.get("SECRET_KEY")

mongo = PyMongo(app)



@app.route("/")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        existing_user = mongo.db.users.find_one(
            {"first": request.form.get("first_name").lower(),
                "last": request.form.get("last_name").lower(),
                "email": request.form.get("email").lower(),
                "password": request.form.get("password").lower()})

        if existing_user:
            # session cookie for role "admin" or "user"
            session["role"] = existing_user["role"]
            # session cookie for users first name
            session["user"] = existing_user["first"]
            flash("user exists")
            return redirect(url_for("userAccount"))
    
        else:
            # invalid password match
            flash("Incorrect Username and/or Password")
            return redirect(url_for("login"))
    
    return render_template("login.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        # check if first_name already exists in db
        existing_user = mongo.db.users.find_one(
            {"first": request.form.get("first_name").lower(),
                "last": request.form.get("last_name").lower()})
        
        if existing_user:
            print(existing_user)
            flash("user exists")
            return redirect(url_for("register"))

        if request.form.get("password") != request.form.get("repeat_password"):
            flash("Password entries must match")
            return redirect(url_for("register"))
        
        register = {
            "first": request.form.get("first_name").lower(),
            "last": request.form.get("last_name").lower(),
            "email": request.form.get("email").lower(),
            "password": generate_password_hash(request.form.get("password")),
            "department": request.form.get("department").lower(),
            "research_group": request.form.get("research_group").lower(),
            "approved": "n",
            "role": "user"
        }
        mongo.db.users.insert_one("register")
        flash("user sucessfully registered")

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


@app.route("/get_user", methods=["GET", "POST"])
def get_user():
    users = mongo.db.users.find()
    if request.method == "POST":
        userStatus = request.form.getlist("userApprove")
        for user in userStatus:
            print(user)
            #get user with _id back as a dictionary existing_user_id
            existing_user_id = mongo.db.users.find_one({"_id": ObjectId(user)})
            print(existing_user_id["approved"])
            newquery = {"_id":ObjectId(user)}
            if existing_user_id["approved"] == "true":
                submit = {"$set": {"approved" : "false"}}
                mongo.db.user.update_one(newquery, submit)
            else:
                submit = {"$set": {"approved" : "true"}}
                mongo.db.user.update_one(newquery, submit)
        users = mongo.db.users.find()

    else:
        return render_template("user.html", users=users)

    return render_template("user.html", users=users)


@app.route("/get_sources")
def get_sources():
    sources = mongo.db.sources.find()
    return render_template("inventory.html", sources=sources)

@app.route("/add_source")
def add_source():
    return render_template("addSource.html")


@app.route("/delete_source")
def delete_source():
    return render_template("deleteSource.html")


@app.route("/update_source")
def update_source():
    return render_template("updateSource.html")


@app.route("/logout")
def logout():

    # remove user from session cookie
    flash("Goodbye, {}".format(session["user"]), "You have been logged out" )
    session.pop("user")
    session.pop("role")
    return render_template("logout.html")


@app.route("/userAccount")
def userAccount():
    session.pop('_flashes', None)
    return render_template("userAccount.html")




if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
            port=int(os.environ.get("PORT")),
            debug=True)