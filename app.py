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
from datetime import datetime


app = Flask(__name__)

app.config["MONGO_DBNAME"] = os.environ.get("MONGO_DBNAME")
app.config["MONGO_URI"] = os.environ.get("MONGO_URI")
app.secret_key = os.environ.get("SECRET_KEY")
mongo = PyMongo(app)

@app.route("/")

@app.route("/login", methods=["GET", "POST"])
def login():
    #
    # Function called when the user first logs in
    #

    # clear any exiting flash messages
    session.pop('_flashes', None)

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
            
            # Add an entry to the user login history
            user = {
                "first": request.form.get("first_name").lower(),
                "last": request.form.get("last_name").lower(),
                "email": request.form.get("email").lower(),
                "login_date": datetime.today().strftime('%d-%m-%y'),
                "logout_date": ""  
            }
            mongo.db.login_history.insert_one(user)
            
            return redirect(url_for("userAccount"))
        else:
            # invalid password match or user name or email
            flash("Incorrect Username and/or Password")
            return redirect(url_for("login"))
    
    return render_template("login.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    # clear any exiting flash messages
    # session.pop('_flashes', None)

    if request.method == "POST":

        # Check if all registration fields have been entered
        if (not((request.form.get("first_name") and not (request.form.get("first_name").isspace())) and
            (request.form.get("last_name") and not (request.form.get("last_name").isspace())) and
            (request.form.get("email") and not (request.form.get("email").isspace())) and
            (request.form.get("password") and not (request.form.get("password").isspace())) and
            (request.form.get("repeat_password") and not (request.form.get("repeat_password").isspace())) and
            (request.form.get("department") and not (request.form.get("department").isspace())) and
                (request.form.get("research_group") and not (request.form.get("research_group").isspace())))):
            flash("Please complete all fields before clicking the submit button")
            return redirect(url_for("register"))
        else:
            print("false")
            # clear any exiting flash messages
            session.pop('_flashes', None)
        
        # check if email already exists in db.
        existing_user = mongo.db.users.find_one(
            {"email": request.form.get("email").lower()})
        
        if existing_user:
            flash("User has already been registered, please try again")
            return redirect(url_for("register"))

        if request.form.get("password") != request.form.get("repeat_password"):
            flash("Password entries must match, please try again")
            return redirect(url_for("register"))
        
        register = {
            "first": request.form.get("first_name").lower(),
            "last": request.form.get("last_name").lower(),
            "email": request.form.get("email").lower(),
            "password": (request.form.get("password")),
            "department": request.form.get("department").lower(),
            "research_group": request.form.get("research_group").lower(),
            "approved": "False",
            "role": "user"
        }
        mongo.db.users.insert_one(register)
        flash("You have sucessfully registered, please wait for your request to be approved")
        return render_template("login.html")

    return render_template("register.html")


@app.route("/usage_report")
def usage_report():
    #
    # Generates reports from the mongodb and renders them for admin user to view
    #
    source_types = mongo.db.sources.find().distinct("isotope")
    
    source_num = []
    for source in source_types:
        source_num.append(mongo.db.sources.count_documents({"isotope": source}))
   
    plt.bar(source_types, source_num)
    plt.savefig('static/assets/sourceUsed.png')
    return render_template("usageReport.html", name="usage plot", url="static/assets/sourceUsed.png")


@app.route("/approve_request", methods=["GET", "POST"])
def approve_request():
    #
    # Called when the admin user wants to see if there are any new source requests to deal with
    #
    
    # clear any exiting flash messages
    session.pop('_flashes', None)
    
    # Check for any requested but not approved sources 
    if len(list( mongo.db.sources.find({"requested": "true"}))) == 0:
        showtable = "false"
        flash("You have no further source requests to approve")
    else:
        showtable = "true"

    existing_sources = mongo.db.sources.find({"requested": "true"})
    alt_existing_sources = mongo.db.sources.find({"requested": "true"})
    return render_template("approveRequest.html", sources=existing_sources, alt_sources=alt_existing_sources, showtable=showtable)


@app.route("/approve_request_resp<source_serial_no>", methods=["GET", "POST"])
def approve_request_resp(source_serial_no):
    #
    # Called when an admin user clicks the button to approve the use of a source
    #
    
    # clear any exiting flash messages
    session.pop('_flashes', None)
    
    # Get mongodb record for source to be loaned
    existing_source = mongo.db.sources.find_one({"serial_number": source_serial_no})
    
    # Create a source loan history entry document in mongodb
    outDate = datetime.today().strftime('%d-%m-%y')
    sourceLoan = {
            "serial_number": source_serial_no,
            "data_out": outDate,
            "date_in": "",
            "user": existing_source["user"],
            "laboratory": existing_source["laboratory"]
        }
    mongo.db.source_history.insert_one(sourceLoan)
    
    # Update the source document in mongodb
    submit = {"approved": "yes",
                "last_used":outDate}
    mongo.db.sources.find_one_and_update({"serial_number": source_serial_no},
            {'$set': submit}, return_document=ReturnDocument.AFTER)
    
    flash("Source Request Appoved")

    return approve_request()


@app.route("/return_source_resp<source_serial_no>", methods=["GET", "POST"])
def return_source_resp(source_serial_no):
    #
    # Called when an admin user returns a source to the inventory
    #  
    
    # clear any exiting flash messages
    session.pop('_flashes', None)
    
    inDate = datetime.today().strftime('%d-%m-%y')

    # Update the  source loan history document in mongodb with return date
    submit = {"date_in" : inDate}
    mongo.db.source_history.find_one_and_update({"serial_number": source_serial_no},
            { '$set': submit }, return_document = ReturnDocument.AFTER)

    # Update the  source document in mongodb with return date and removal approval status
    submit = {"last_used" : inDate,
                "approved" : "no",
                "requested" : "false",
                "user" : ""
                }
    mongo.db.sources.find_one_and_update({"serial_number": source_serial_no},
            { '$set': submit }, return_document = ReturnDocument.AFTER)
    
    flash("Source Returned To Inventory")
    return approve_request()


@app.route("/get_userb/<user_id>", methods=["GET", "POST"])
def get_userb(user_id):
    #
    # Called when an admin user approves a new account
    #
    if request.method == "GET":
        existing_user = mongo.db.users.find_one({"_id": ObjectId(user_id)})
        if existing_user["approved"] == "True":
            submit = {"approved": "False"}
        else:
            submit = {"approved": "True"}
        
        # pymongo update has been deprecated use find_one_and_update
        mongo.db.users.find_one_and_update({"_id": ObjectId(user_id)},
            { '$set': submit }, return_document = ReturnDocument.AFTER)
        flash("User Successfully Approved")
    users = mongo.db.users.find()
    alt_users = mongo.db.users.find()
    return render_template("user.html", users=users, alt_user=alt_users)



@app.route("/get_userc/<user_id>", methods=["GET", "POST"])
def get_userc(user_id):
    #
    # Called when an admin user gives admin rights to another user
    #
    existing_user = mongo.db.users.find_one({"_id": ObjectId(user_id)})
    if existing_user["role"] == "admin":
        submit = {"role": "user"}
    else:
        submit = {"role": "admin"}
        
    mongo.db.users.find_one_and_update({"_id": ObjectId(user_id)},
        { '$set': submit }, return_document = ReturnDocument.AFTER)
    flash("User role successfully updated")
    users = mongo.db.users.find()
    alt_users=mongo.db.users.find()
    return render_template("user.html", users=users, alt_users=alt_users)



@app.route("/get_user")
def get_user():
    users=mongo.db.users.find()
    alt_users=mongo.db.users.find()
    return render_template("user.html", users=users, alt_users=alt_users) 


@app.route("/get_sources")
def get_sources():
    # Guidance on the rewinding/reseting of the pymongo cursor unclear
    # hence use 2 instances of the cursor one for each view (large 
    # width/reduced width screen size)
    sources = mongo.db.sources.find()
    alt_sources = mongo.db.sources.find()
    return render_template("inventory.html", sources=sources, alt_sources=alt_sources)


@app.route("/add_source", methods=["GET", "POST"])
def add_source():
    #
    # Called when an admin user adds a new source to the source inventory
    #
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
        alt_sources = mongo.db.sources.find()
        return render_template("inventory.html", sources=sources, alt_sources=alt_sources)
  
    return render_template("addSource.html")



@app.route("/source_request", methods=["GET", "POST"])
def source_request():
    #
    # Action on selecting the SOURCE REQUEST option
    #
    query = request.form.get("query")
    mode = "request"
    if query:
        sources = list(mongo.db.sources.find({"$text": {"$search": query}}))
        alt_sources = list(mongo.db.sources.find({"$text": {"$search": query}}))
        showsources = "true"
        return render_template("sourceRequest.html", showsources=showsources, alt_sources=alt_sources, sources=sources, mode=mode)
    else:
        showsources = "false"
        sources = ""
        alt_sources=" "
        return render_template("sourceRequest.html", showsources=showsources, sources=sources, alt_sources=alt_sources, mode=mode)




@app.route("/req_source_conf/<source_serial_no>" , methods=["GET", "POST"])
def req_source_conf(source_serial_no):
    #
    # Action on clicking the REQUEST button on the SOURRCE REQUEST Page 
    #
    sources=mongo.db.sources.find_one({"serial_number": source_serial_no})
    alt_sources=mongo.db.sources.find_one({"serial_number": source_serial_no})

    # Update the source record
    submit = {"requested": "true", "user": session["user"]} 
    mongo.db.sources.update({"serial_number": source_serial_no},{"$set": submit})
    
    flash("Source has been requested - please wait for your request to be approved")

    showsources = "false"
    sources = ""
    mode ="request"
    return render_template("sourceRequest.html", showsources=showsources, sources=sources, alt_sources=alt_sources, mode=mode)


@app.route("/del_source_conf/<source_serial_no>" , methods=["GET", "POST"])
def del_source_conf(source_serial_no):
    #
    # Gets source data from the mongo db and generates a table
    #

    mongo.db.sources.delete_one({"serial_number": source_serial_no})
    sources = mongo.db.sources.find()
    alt_sources = mongo.db.sources.find()
    return render_template("inventory.html", sources=sources, alt_sources=alt_sources)


@app.route("/update_source", methods=["GET", "POST"])
def update_source():
    #
    # called when the admin user selects a source for update via a query
    #

    query = request.form.get("query")
    mode = "update"
    if query:
        sources = list(mongo.db.sources.find({"$text": {"$search": query}}))
        alt_sources = list(mongo.db.sources.find({"$text": {"$search": query}}))
        showsources = "true"
        return render_template("sourceRequest.html", showsources=showsources, sources=sources, alt_sources=alt_sources, mode=mode)
    else:
        showsources = "false"
        sources = ""
        alt_sources =" "
        return render_template("sourceRequest.html", showsources=showsources, sources=sources, alt_sources=alt_sources, mode=mode)



@app.route("/delete_source", methods=["GET", "POST"])
def delete_source():
    #
    # called when the admin user selects a source for deletion via a query
    #

    query = request.form.get("query")
    mode = "delete"
    if query:
        # line of code from Code Institute tuition Data "Centric Design Mini Project"
        sources = list(mongo.db.sources.find({"$text": {"$search": query}}))
        alt_sources = list(mongo.db.sources.find({"$text": {"$search": query}}))
        showsources = "true"
        return render_template("sourceRequest.html", showsources=showsources, sources=sources, alt_sources=alt_sources, mode=mode)
    else:
        showsources = "false"
        sources = ""
        alt_sources =" "
        return render_template("sourceRequest.html", showsources=showsources, sources=sources, alt_sources=alt_sources, mode=mode)



@app.route("/update_source_resp/<source_serial_no>", methods=["GET", "POST"])
def update_source_resp(source_serial_no):
    #
    #
    #
    existing_source = mongo.db.sources.find_one({"serial_number": source_serial_no})
    mode = "update"
    return render_template("addSource.html", mode=mode, existing_source=existing_source )


@app.route("/delete_source_resp/<source_serial_no>", methods=["GET", "POST"])
def delete_source_resp(source_serial_no):
    #
    # Called prior to user clicking button to delete a source from the mongo db 
    #      
    
    # check if source serial number already exists in db
    existing_source = mongo.db.sources.find_one({"serial_number": source_serial_no})    
    mode = "delete"
    flash("You are about to delete", source_serial_no)    
    return render_template("addSource.html", mode=mode, existing_source=existing_source)


@app.route("/logout")
def logout():
    #
    # Called when a user logs out of a session
    #

    # Add an entry to the user login history
    user = {"logout_date": datetime.today().strftime('%d-%m-%y')}
    mongo.db.login_history.update({"first": session["user"]},{"$set": user})
    # Remove user from session cookie
    # Code line from Code Institute Mini Project 
    flash("Goodbye, {}".format(session["user"]), "You have been logged out" )
    session.pop("user")
    session.pop("role")
    return render_template("login.html")


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
    
    # Get list of sources held by the user
    userfirst = existing_user["first"]
    loanSources = mongo.db.sources.find({"user": userfirst})

    return render_template("userAccount.html", user=existing_user, sources=loanSources)

if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
            port=int(os.environ.get("PORT")),
            debug=True)