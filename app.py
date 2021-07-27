import os
import re
import math
import matplotlib.pyplot as plt
import numpy as np
import pymongo

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

    # Ensure only login and register nav bar options are available
    if session.get("in_use"):
        session.pop("in_use")
    
    if request.method == "POST":
        existing_user = mongo.db.users.find_one(
                {"email": request.form.get("email").lower(),
                    "password": request.form.get("password").lower()})

        if existing_user:
            # Check if user already has an open session
            # if existing_user["status"] == "logged_out":
                # Check if users account has been approved
                if existing_user["approved"] == "approved":
                    # session cookie for role "admin" or "user"
                    session["role"] = existing_user["role"]
                    # session cookie for users first name
                    session["user"] = existing_user["first"]
                    # session cookie for in_use
                    session["in_use"] = True

                    # Set user status to logged out
                    user_status = {"status": "logged_in"}
                    mongo.db.users.find_one_and_update({"first": session["user"]},
                            {'$set': user_status}, return_document=ReturnDocument.AFTER)
                    
                    # Add an entry to the user login history
                    login_entry = {
                        "first": existing_user["first"].lower(),
                        "last": existing_user["last"].lower(),
                        "email": request.form.get("email").lower(),
                        "login_date": datetime.today().strftime('%d-%m-%y'),
                        "logout_date": ""
                    }
                    mongo.db.login_history.insert_one(login_entry)
                    return redirect(url_for("userAccount"))
                else:
                    flash("Account not approved or suspended")
                    return redirect(url_for("login"))
            # else:
            #    flash("Please log out before logging in again")
            #    return redirect(url_for("login"))
        else:
            # invalid password match or user name or email
            flash("Incorrect Username and/or Password")
            return redirect(url_for("login"))

    return render_template("login.html")


@app.route("/logout")
def logout():
    #
    # Called when a user or admin logs out of a session
    #

    # Add date to the user login history
    user_history = {"logout_date": datetime.today().strftime('%d-%m-%y')}
    mongo.db.login_history.find_one_and_update({"first": session["user"]},
            {'$set': user_history}, return_document=ReturnDocument.AFTER)
    
    # Set user status to logged out
    user_status = {"status": "logged_out"}
    mongo.db.users.find_one_and_update({"first": session["user"]},
            {'$set': user_status}, return_document=ReturnDocument.AFTER)

    # Code line from Code Institute Mini Project
    flash("Goodbye, {}".format(session["user"]), "You have been logged out")
    # Remove user from session cookies if active
    if session.get("user"):
        session.pop("user")
    if session.get("role"):
        session.pop("role")
    if session.get("in_use"):
        session.pop("in_use")
    
    return render_template("login.html")


@app.route("/register", methods=["GET", "POST"])
def register():

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
            "approved": "approve",
            "role": "user",
            "approved_date": "",
            "deleted_date":""
        }
        mongo.db.users.insert_one(register)
        flash("You have sucessfully registered, please wait for your request to be approved")
        return render_template("login.html")

    return render_template("register.html")

#-------------------------Report Generation-----------------------------------
@app.route("/usage_report")
def usage_report():
    #
    # Generates reports from the mongodb and renders them for admin user to view
    #

    # Determine sources of isotopes on inventory
    source_types = mongo.db.sources.find().distinct("isotope")
    source_num = []
    for source in source_types:
        source_num.append(mongo.db.sources.count_documents({"isotope": source}))
    
    # Determine Logins per day
    logins = mongo.db.login_history.find().distinct("login_date")
    login_num = []
    for login in logins:
        login_num.append(mongo.db.login_history.count_documents({"login_date": login}))

    # Determine source usage by serial number
    source_loans = mongo.db.source_history.find().distinct("serial_number")
    loans_num = []
    for loans in source_loans:
        loans_num.append(mongo.db.source_history.count_documents({"serial_number": loans}))

    # Page only accessible for admin users
    if session["role"] == "admin":
        plt.bar(source_types, source_num, color='green')
        plt.title("Sources by Isotope") 
        plt.savefig('static/assets/sourceUsed.png')
        plt.close()

        plt.bar(logins, login_num, color='blue')
        plt.title("User Logins by Day")  
        plt.savefig('static/assets/loginHistory.png')
        plt.close()

        plt.bar(source_loans, loans_num, color='red')
        plt.title("Source Loans by Serial Number")  
        plt.savefig('static/assets/loanHistory.png')
        plt.close()

        return render_template("usageReport.html", name="usage plot",
            url1="static/assets/sourceUsed.png",
            url2="static/assets/loginHistory.png",
            url3="static/assets/loanHistory.png")
    else:
        return render_template("errorPage.html")


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

    existing_sources = list(mongo.db.sources.find({"requested": "true"}))
    return render_template("approveRequest.html", sources=existing_sources,
        showtable=showtable)


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
    # Called when an admin user approves a new account or suspends/re-approves
    # an account. User approved state starts at "appove" then toggles between
    # "approved" and "suspended" 
    #

    existing_user = mongo.db.users.find_one({"_id": ObjectId(user_id)})

    # User cannot action his/her own account
    if existing_user["first"] == session["user"]:
        flash("You cannot action your own user account")
    else:
        # Admin user approves first time registration 
        if existing_user["approved"] == "approve":
            submit = {"approved": "approved",
                      "approved_date": datetime.today().strftime('%d-%m-%y'),
                      "remove_date": ""
                    }
            flash("User Successfully Approved")

        # Admin user suspends users account
        if existing_user["approved"] == "approved":
            submit = {"approved": "suspended",
                      "approved_date": "",
                      "remove_date": datetime.today().strftime('%d-%m-%y')
                    }
            flash("User Successfully Suspended")

        # Admin user reinstates users account
        if existing_user["approved"] == "suspended":
            submit = {"approved": "approved",
                      "approved_date": datetime.today().strftime('%d-%m-%y'),
                      "remove_date": ""
                     }              
            flash("User Successfully Approved")

        # pymongo update has been deprecated use find_one_and_update
        mongo.db.users.find_one_and_update({"_id": ObjectId(user_id)},
            { '$set': submit }, return_document = ReturnDocument.AFTER)

    users = list(mongo.db.users.find())
    return render_template("user.html", users=users)


@app.route("/get_userc/<user_id>", methods=["GET", "POST"])
def get_userc(user_id):
    #
    # Called when an admin user gives admin rights to another user
    #
    
    existing_user = mongo.db.users.find_one({"_id": ObjectId(user_id)})
    
    # User cannot action his/her own account
    if existing_user["first"] == session["user"]:
        flash("You cannot action your own user account")
    else:
        # Admin user toggles another user account between admin/user roles
        if existing_user["role"] == "admin":
            submit = {"role": "user"}
        else:
            submit = {"role": "admin"}    
        mongo.db.users.find_one_and_update({"_id": ObjectId(user_id)},
            { '$set': submit }, return_document = ReturnDocument.AFTER)
        flash("User role successfully updated")
    
    users = list(mongo.db.users.find())
    return render_template("user.html", users=users)


@app.route("/get_userdelete/<user_id>", methods=["GET", "POST"])
def get_userdelete(user_id):
    #
    # Called when an admin user deletes a normal user account
    #
    existing_user = mongo.db.users.find_one({"_id": ObjectId(user_id)})
    
    # User cannot delete his/her own account 
    if existing_user["first"] == session["user"]:
        flash("You cannot delete your own user account")

    # Admin user cannot be deleted/removed
    elif existing_user["role"] == "admin":
        flash("You cannot delete an Admin user")
    
    # User account must be suspended before it can be deleted
    elif existing_user["approved"] == "approved" or existing_user["approved"] == "approve":
        flash("A user account must be suspended for it to be deleted")

    else: 
        mongo.db.users.delete_one({"_id": ObjectId(user_id)})
        flash("user account sucessfuly deleted")

    users = list(mongo.db.users.find())
    return render_template("user.html", users=users)


@app.route("/get_user")
def get_user():
    #
    # Called to display a complete table of all users with eiter admin or user role
    #

    # Restrict access to admin users only
    if session["role"] == "admin":   
        users = list(mongo.db.users.find())
        return render_template("user.html", users=users) 
    else:
        return render_template("errorPage.html")

@app.route("/get_sources")
def get_sources():
    # 
    # Called when the full source inventory is to be displayed
    # Calculates updated source activity 
    # 

    sources = list(mongo.db.sources.find())
    
    for source in sources:
        serial_number=(source["serial_number"])
        origin_act=float(source["original_activity"])
        date_out=source["activation_date"]
        half_life=float(source["half_life"])

        # datetime.datetime.strptime only supported by date time 
        # strftime used else where and requires the datetime component from datetime
        import datetime
        delta_years = (((datetime.datetime.now() - datetime.datetime.strptime(date_out, '%d-%m-%y')).days)/365.25)
        from datetime import datetime
        
        # Calculate new activity using equation for radioactive decay
        new_act=str(round(origin_act*math.exp(((-1*math.log(2)*delta_years)/half_life)),2))
        
        source_new_act = {"activity_now": new_act}
        mongo.db.sources.find_one_and_update({"serial_number": serial_number},
            {'$set': source_new_act}, return_document=ReturnDocument.AFTER)
    
    # Restrict access to admin users only
    if session["role"] == "admin":    
        return render_template("inventory.html", sources=sources)
    else:
        return render_template("errorPage.html")

@app.route("/add_source", methods=["GET", "POST"])
def add_source():
    #
    # Called when an admin user adds a new source to the source inventory
    # or when an admin user updates an exiting source
    #

    if request.method == "POST":
        # Get source from mongo db
        existing_source = mongo.db.sources.find_one(
        {"serial_number": request.form.get("serial_number")})

        # Get isotope half life
        isotope_half_life = mongo.db.isotope_category.find_one({"isotope": request.form.get("isotope")})
        
        # check if source serial number already exists in db
        if existing_source:
            updateSource = {
            "serial_number": request.form.get("serial_number"),
            "department": request.form.get("department"),
            "laboratory": request.form.get("laboratory"),
            "location": request.form.get("location"),
            "isotope": request.form.get("isotope"),
            "half_life": isotope_half_life,
            "half_life_units": "years",
            "original_activity": request.values.get("original_activity"),
            "original_activity_units": request.values.get("original_activity_units"),
            "activation_date": request.values.get("activation_date"),
            "type": request.values.get("encapsulation"),
            }
            mongo.db.sources.find_one_and_update({"serial_number": request.form.get("serial_number")},
            { '$set': updateSource }, return_document = ReturnDocument.AFTER)
            flash("Source sucessfully updated")
        else:
            newSource = {
            "serial_number": request.form.get("serial_number"),
            "department": request.form.get("department"),
            "laboratory": request.form.get("laboratory"),
            "location": request.form.get("location"),
            "isotope": request.form.get("isotope"),
            "half_life": isotope_half_life["isotope"][1],
            "half_life_units": "years",
            "original_activity": request.values.get("original_activity"),
            "original_activity_units": request.values.get("original_activity_units"),
            "activation_date": request.values.get("activation_date"),
            "type": request.values.get("encapsulation"),
            "last_used":"",
            "approved":"no",
            "requested":"false",
            "user":""
            }
            mongo.db.sources.insert_one(newSource)
            flash("New source sucessfully added to inventory")
        
        # Confirm that user has admin rights and can render requested page 
        if session["role"] == "admin":
            sources = list(mongo.db.sources.find())
            return render_template("inventory.html", sources=sources )
        else:
            return render_template("errorPage.html")
    
    # Restrict access to admin users only
    if session["role"] == "admin":
        #No post setup html page for adding a new source
        security_codes = mongo.db.security_group.find()
        departments = mongo.db.departments.find()
        laboratories = mongo.db.laboratories.find()
        locations = mongo.db.locations.find()
        encapsulations = mongo.db.encapsulations.find()
        isotope_category = list(mongo.db.isotope_category.find())
        mode = "add"
        return render_template("addSource.html",security_codes=security_codes,
            departments=departments, laboratories= laboratories,
            locations=locations, mode=mode, encapsulations=encapsulations,
            isotope_category=isotope_category )
    else:
        return render_template("errorPage.html")


@app.route("/source_request", methods=["GET", "POST"])
def source_request():
    #
    # Action on selecting the SOURCE REQUEST option
    # Action open to users and admin
    #
    query = request.form.get("query")
    mode = "request"
    if query:
        # Find collection of seached sources not already requested
        sources = list(mongo.db.sources.find({"$and":[{"$text": {"$search": query}}, {"requested":"false"}]}))
        showsources = "true"
        return render_template("sourceRequest.html", showsources=showsources, sources=sources, mode=mode)
    else:
        showsources = "false"
        sources = []
        return render_template("sourceRequest.html", showsources=showsources, sources=sources, mode=mode)


@app.route("/del_source_req/<source_serial_no>" , methods=["GET", "POST"])
def del_source_req(source_serial_no):
    #
    # Action when user deletes a source request before authorised by admin
    # Action open to users and admin
    #
    submit = {"approved": "no",
            "requested": "false",
            "user": ""}

    mongo.db.sources.find_one_and_update({"serial_number": source_serial_no},
            { '$set': submit }, return_document = ReturnDocument.AFTER)

    # Get list of sources held by the user
    userfirst = session["user"]
    loanSources = list(mongo.db.sources.find({"user": userfirst}))
    return redirect(url_for("userAccount"))


@app.route("/req_source_conf/<source_serial_no>" , methods=["GET", "POST"])
def req_source_conf(source_serial_no):
    #
    # Action on clicking the REQUEST button on the SOURRCE REQUEST Page
    # Action open to users and admin
    #
    sources=list(mongo.db.sources.find_one({"serial_number": source_serial_no}))

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
    #
    # Gets source data from the mongo db and generates a table
    #

    # Restrict access to admin users only
    if session["role"] == "admin":
        mongo.db.sources.delete_one({"serial_number": source_serial_no})
        sources = list(mongo.db.sources.find())
        return render_template("inventory.html", sources=sources)
    else:
        return render_template("errorPage.html")


@app.route("/update_source", methods=["GET", "POST"])
def update_source():
    #
    # called when the admin user selects a source for update via a query
    #

    # Restrict access to admin users only
    if session["role"] == "admin":
        query = request.form.get("query")
        mode = "update"
        if query:
            sources = list(mongo.db.sources.find({"$text": {"$search": query}}))
            showsources = "true"
            return render_template("sourceRequest.html", showsources=showsources, sources=sources, mode=mode)
        else:
            showsources = "false"
            sources = []
            return render_template("sourceRequest.html", showsources=showsources, sources=sources, mode=mode)
    else:
        return render_template("errorPage.html")


@app.route("/delete_source", methods=["GET", "POST"])
def delete_source():
    #
    # called when the admin user selects a source for deletion via a query
    #

    # Restrict access to admin users only
    if session["role"] == "admin":
        query = request.form.get("query")
        mode = "delete"
        if query:
            # line of code from Code Institute tuition Data "Centric Design Mini Project"
            sources = list(mongo.db.sources.find({"$text": {"$search": query}}))
            showsources = "true"
            return render_template("sourceRequest.html", showsources=showsources, sources=sources, mode=mode)
        else:
            showsources = "false"
            sources = []
            return render_template("sourceRequest.html", showsources=showsources, sources=sources, mode=mode)
    else:
        return render_template("errorPage.html")


@app.route("/update_source_resp/<source_serial_no>", methods=["GET", "POST"])
def update_source_resp(source_serial_no):
    #
    # Called when data relating to a source requires update
    #

    # Restrict access to admin users only
    if session["role"] == "admin":
        existing_source = mongo.db.sources.find_one({"serial_number": source_serial_no})
        mode = "update"
        security_codes = mongo.db.security_group.find()
        departments= mongo.db.departments.find()
        laboratories = mongo.db.laboratories.find()
        locations = mongo.db.locations.find()
        encapsulations = mongo.db.encapsulations.find()

        return render_template("addSource.html", mode=mode, existing_source=existing_source,
                security_codes=security_codes, departments=departments,
                locations=locations, laboratories=laboratories,
                encapsulations=encapsulations )
    else:
        return render_template("errorPage.html")


@app.route("/delete_source_resp/<source_serial_no>", methods=["GET", "POST"])
def delete_source_resp(source_serial_no):
    #
    # Called prior to user clicking button to delete a source from the mongo db 
    #      
    
    # Restrict access to admin users only
    if session["role"] == "admin":
        # check if source serial number already exists in db
        existing_source = mongo.db.sources.find_one({"serial_number": source_serial_no})    
        mode = "delete"
        flash("You are about to delete", source_serial_no)    
        return render_template("addSource.html", mode=mode, existing_source=existing_source)
    else:
        return render_template("errorPage.html")


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
    loanSources = list(mongo.db.sources.find({"user": userfirst}))
    return render_template("userAccount.html",
            user=existing_user, usersources=loanSources)

#-------------------------Manage isotope types------------------------
@app.route("/manage_isotopes", methods=["GET", "POST"])
def manage_isotopes():
    #
    #  Called to list out isotope types to the admin user
    #
    if request.method == "POST":
        isotope_entry = {
                        "isotope": request.form.get("isotope"),
                        "halflife": request.form.get("halflife")
                        }
        mongo.db.isotope_category.insert_one(isotope_entry)

    # get isotope list   
    if session["role"] == "admin":
        isotopes = list(mongo.db.isotope_category.find())   
        return render_template("isotopeTypes.html", isotopes=isotopes)
    else:
        return render_template("errorPage.html")


@app.route("/delete_isotope_resp/<isotope_id>", methods=["GET", "POST"])
def delete_isotope_resp(isotope_id):
    #
    # Called to delete an isotope from the list in mongo db 
    #
    mongo.db.isotope_category.delete_one({"_id": ObjectId(isotope_id)})     
    return redirect(url_for("manage_isotopes"))

#-------------------------Error Handlers------------------------------
@app.errorhandler(404) 
def invalid_route(e):
    #
    # Handles 404 page not found error 
    # 
    return render_template("404error.html")

#-------------------------Main Loop-----------------------------------
if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
            port=int(os.environ.get("PORT")),
            debug=True)