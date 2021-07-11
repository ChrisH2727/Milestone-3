import os
import re
import matplotlib.pyplot as plt
import numpy as np

from flask import (
    Flask, flash, render_template,
    redirect, request, session, url_for)
from flask_pymongo import PyMongo
from pymongo import ReturnDocument
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
            {"first": request.form.get("first_name"),
                "last": request.form.get("last_name")})
        
        if existing_user:
            print(existing_user)
            flash("user exists")
            return redirect(url_for("register"))

        if request.form.get("password") != request.form.get("repeat_password"):
            flash("Password entries must match")
            return redirect(url_for("register"))
        
        register = {
            "first": request.form.get("first_name"),
            "last": request.form.get("last_name"),
            "email": request.form.get("email"),
            "password": (request.form.get("password")),
            "department": request.form.get("department"),
            "research_group": request.form.get("research_group"),
            "approved": "False",
            "role": "user"
        }
        mongo.db.users.insert_one(register)
        flash("user sucessfully registered")

    return render_template("register.html")




@app.route("/usage_report")
def usage_report():
    source_types = mongo.db.sources.find().distinct("isotope")
    
    source_num = []
    for source in source_types:
        source_num.append(mongo.db.sources.count_documents({"isotope": source}))
   
    plt.bar(source_types, source_num)
    plt.savefig('static/assets/sourceUsed.png')
    return render_template("usageReport.html", name="usage plot", url="static/assets/sourceUsed.png")



@app.route("/approve_request")
def approve_request():
    existing_sources = mongo.db.sources.collection.find({ "$and":[
            {"sources":{"$requested": "true"}} , {"sources":{"$approved": "no"}}]})
            
    return render_template("approveRequest.html", sources=existing_sources)


@app.route("/get_userb/<user_id>", methods=["GET", "POST"])
def get_userb(user_id):
    if request.method == "GET":
        existing_user = mongo.db.users.find_one({"_id": ObjectId(user_id)})
        if existing_user["approved"] == "True":
            submit = {"approved": "False"}
        else:
            submit = {"approved": "True"}
        
        mongo.db.users.find_one_and_update({"_id": ObjectId(user_id)},
            { '$set': submit }, return_document = ReturnDocument.AFTER)
        flash("User Successfully Approved")
    users = mongo.db.users.find()
    return render_template("user.html" , users=users)



@app.route("/get_userc/<user_id>", methods=["GET", "POST"])
def get_userc(user_id):
    if request.method == "GET":
        existing_user = mongo.db.users.find_one({"_id": ObjectId(user_id)})
        if existing_user["role"] == "admin":
            submit = {"role": "user"}
        else:
            submit = {"role": "admin"}
        
        mongo.db.users.find_one_and_update({"_id": ObjectId(user_id)},
            { '$set': submit }, return_document = ReturnDocument.AFTER)
        flash("User role successfully updated")
    users = mongo.db.users.find()
    return render_template("user.html" , users=users)



@app.route("/get_user")
def get_user():
    users = mongo.db.users.find()
    return render_template("user.html", users=users) 


@app.route("/get_sources")
def get_sources():
    sources = mongo.db.sources.find()
    return render_template("inventory.html", sources=sources)


@app.route("/add_source", methods=["GET", "POST"])
def add_source():
    if request.method == "POST":
        # check if source serial number already exists in db
        existing_source = mongo.db.sources.find_one(
            {"serial_number": request.form.get("serial_number")})

        newSource = {
            "serial_number": request.form.get("serial_number"),
            "department": request.form.get("department"),
            "laboratory": request.form.get("laboratory"),
            "location": request.form.get("location"),
            "isotope": request.form.get("isotope"),
            "half_life": request.form.get("half_life"),
            "half_life_units": request.values.get("half_life_units")
        }

        if existing_source:
            existing_source_id = existing_source["_id"]
            print("update")

            newSourceTemp = {
                "serial_number": request.form.get("serial_number"),
                "department": request.form.get("department")
            }

            mongo.db.sources.find_one_and_update({"_id": ObjectId(existing_source_id)},
            { '$set': newSourceTemp }, return_document = ReturnDocument.AFTER)
            flash("Source sucessfully updated")
        else:
            mongo.db.sources.insert_one(newSource)
            flash("New source sucessfully added to inventory")
    
        sources = mongo.db.sources.find()
        return render_template("inventory.html", sources=sources)
  
    return render_template("addSource.html")


#
# Action on selecting the SOURCE REQUEST option
#
@app.route("/source_request", methods=["GET", "POST"])
def source_request():
    query = request.form.get("query")
    mode = "request"
    if query:
        sources = list(mongo.db.sources.find({"$text": {"$search": query}}))
        showsources = "true"
        return render_template("sourceRequest.html", showsources=showsources, sources=sources, mode=mode)
    else:
        showsources = "false"
        sources = ""
        return render_template("sourceRequest.html", showsources=showsources, sources=sources, mode=mode)



#
# Action on clicking the REQUEST button on the SOURRCE REQUEST Page 
#
@app.route("/req_source_conf/<source_serial_no>" , methods=["GET", "POST"])
def req_source_conf(source_serial_no):
    source = mongo.db.sources.find_one({"serial_number": source_serial_no})
    
    # Update the source record
    submit = {"requested": "true", "user": session["user"]} 
    mongo.db.sources.update({"serial_number": source_serial_no},{"$set": submit})
    
    flash("Source has been requested - please wait for your request to be approved")

    showsources = "false"
    sources = ""
    mode ="request"
    return render_template("sourceRequest.html", showsources=showsources, sources=sources, mode=mode)


@app.route("/del_source_conf/<source_serial_no>" , methods=["GET", "POST"])
def del_source_conf(source_serial_no):
    mongo.db.sources.delete_one({"serial_number": source_serial_no})
    sources = mongo.db.sources.find()
    return render_template("inventory.html", sources=sources)



@app.route("/update_source", methods=["GET", "POST"])
def update_source():
    query = request.form.get("query")
    mode = "update"
    if query:
        sources = list(mongo.db.sources.find({"$text": {"$search": query}}))
        showsources = "true"
        return render_template("sourceRequest.html", showsources=showsources, sources=sources, mode=mode)
    else:
        showsources = "false"
        sources = ""
        return render_template("sourceRequest.html", showsources=showsources, sources=sources, mode=mode)



@app.route("/delete_source", methods=["GET", "POST"])
def delete_source():
    query = request.form.get("query")
    mode = "delete"
    if query:
        sources = list(mongo.db.sources.find({"$text": {"$search": query}}))
        showsources = "true"
        return render_template("sourceRequest.html", showsources=showsources, sources=sources, mode=mode)
    else:
        showsources = "false"
        sources = ""
        return render_template("sourceRequest.html", showsources=showsources, sources=sources, mode=mode)




@app.route("/update_source_resp/<source_serial_no>", methods=["GET", "POST"])
def update_source_resp(source_serial_no):
    existing_source = mongo.db.sources.find_one({"serial_number": source_serial_no})
    mode = "update"
    return render_template("addSource.html", mode=mode, existing_source=existing_source )


@app.route("/delete_source_resp/<source_serial_no>", methods=["GET", "POST"])
def delete_source_resp(source_serial_no):     
    # check if source serial number already exists in db
    existing_source = mongo.db.sources.find_one({"serial_number": source_serial_no})    
    mode = "delete"
    flash("You are about to delete", source_serial_no)    
    return render_template("addSource.html", mode=mode, existing_source=existing_source)


@app.route("/logout")
def logout():

    # remove user from session cookie
    flash("Goodbye, {}".format(session["user"]), "You have been logged out" )
    session.pop("user")
    session.pop("role")
    return render_template("logout.html")


@app.route("/userAccount", methods=["GET", "POST"])
def userAccount():

    # User already logged in so use session cookie as key to user details
    existing_user = mongo.db.users.find_one({"first": session["user"]})

    user_id = existing_user["_id"]
    
    if request.method == "POST":

        if request.form.get("password") != request.form.get("repeat_password"):
            flash("Please ensure that that your password entries match")
        else:
            submit = {"password": request.form.get("password"),
                "department": request.form.get("department").lower(),
                "research_group": request.form.get("research_group").lower()}

            mongo.db.users.find_one_and_update({"_id": ObjectId(user_id)},
                { '$set': submit }, return_document = ReturnDocument.AFTER)
        
            flash("Your account details have been successfully updated")
    
    existing_user = mongo.db.users.find_one({"_id": ObjectId(user_id)})    
    
    return render_template("userAccount.html", user=existing_user)




if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
            port=int(os.environ.get("PORT")),
            debug=True)