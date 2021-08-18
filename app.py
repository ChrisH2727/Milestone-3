import os
import math
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime
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
# -------------------------User Login and Registration--------
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
            {"email": request.form.get("email").lower()})

        if existing_user:
            if check_password_hash(
                    existing_user["password"], request.form.get("password")):

                # Check if users account has been approved
                if existing_user["approved"] == "approved":

                    # Check if user already logged in
                    if session.get("user"):
                        flash("User already logged in, please log out")
                        return render_template("login.html")

                    else:
                        # Set up session variable for role "admin" or "user"
                        # Set up session variable for user first name and email
                        session["role"] = existing_user["role"]
                        session["user"] = existing_user["first"]
                        session["email"] = existing_user["email"]

                        # Set up session variable for in_use ensures that
                        # menu only display navigation bar to registered users
                        session["in_use"] = True

                        # Add an entry to the user login history
                        login_entry = {
                            "first": existing_user["first"].lower(),
                            "last": existing_user["last"].lower(),
                            "email": request.form.get("email").lower(),
                            "login_date": datetime.today().strftime(
                                '%d-%m-%y')
                        }
                        mongo.db.login_history.insert_one(login_entry)
                        return redirect(url_for("userAccount"))
                else:
                    flash("Account not approved or suspended")
                    return redirect(url_for("login"))
            else:
                flash("Incorrect password")
                return redirect(url_for("login"))
        else:
            flash("Incorrect username please register")
            return redirect(url_for("login"))

    return render_template("login.html")


@app.route("/logout")
def logout():
    #
    # Called when a user or admin logs out of a session
    #

    if not session.get("user"):
        return render_template("404error.html")

    # Code line from Code Institute Mini Project
    flash("Goodbye {} you have logged out".format(
        (session["user"]).capitalize()))
    # Remove user from session cookies if active
    if session.get("user"):
        session.pop("user")
    if session.get("role"):
        session.pop("role")
    if session.get("in_use"):
        session.pop("in_use")
    if session.get("email"):
        session.pop("email")

    return render_template("login.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    #
    # Called to register a new user
    #

    if request.method == "POST":
        # check if user email already exists in db.
        existing_user = mongo.db.users.find_one(
            {"email": request.form.get("email").lower()})

        if existing_user:
            flash("User has already been registered, please try again")
            return redirect(url_for("register"))

        # Check for repeat password match
        if request.form.get("password") != request.form.get("repeat_password"):
            flash("Password entries must match, please try again")
            return redirect(url_for("register"))

        register = {
            "first": request.form.get("first_name").lower(),
            "last": request.form.get("last_name").lower(),
            "email": request.form.get("email").lower(),
            "password": generate_password_hash(request.form.get("password")),
            "department": request.form.get("department").lower(),
            "research_group": request.form.get("research_group").lower(),
            "approved": "approve",
            "role": "user",
            "approved_date": "",
            "deleted_date": ""
        }
        mongo.db.users.insert_one(register)
        flash("You have sucessfully registered, please\
                wait for your request to be approved")
        return render_template("login.html")

    # Get all departments and check is collection is empty
    if mongo.db.departments.count_documents({}) != 0:
        departments = list(
            mongo.db.departments.find())
    else:
        flash("Database error detected, please refer to admin user")
        departments = []
    return render_template("register.html", departments=departments)

# -------------------------Report Generation-----------------------------------


@app.route("/usage_report")
def usage_report():
    #
    # Generates reports from the mongodb and renders them for admin
    # users to view.
    #

    # Detect 404 page error
    if not session.get("user"):
        return render_template("404error.html")

    # Check if user has access to this page
    if (session["role"] == "user"):
        return render_template("errorPage.html")

    # Determine sources of isotopes on inventory
    source_types = mongo.db.sources.find().distinct("isotope")
    source_num = []
    for source in source_types:
        source_num.append(
            mongo.db.sources.count_documents({"isotope": source}))

    # Determine Logins per day
    logins = mongo.db.login_history.find().distinct("login_date")
    login_num = []
    for login in logins:
        login_num.append(mongo.db.login_history.count_documents(
            {"login_date": login}))

    # Determine source usage by serial number
    source_loans = list(
        mongo.db.source_history.find().distinct("serial_number"))

    loans_num = []
    for loans in source_loans:
        loans_num.append(mongo.db.source_history.count_documents(
            {"serial_number": loans}))

    try:
        # generate plots
        plt.bar(source_types, source_num, color='green')
        plt.yticks(np.arange(0, 5, 1))
        plt.title("Sources by Isotope")
        plt.savefig('static/assets/sourceUsed.png')
        plt.close()

        plt.bar(logins, login_num, color='blue')
        plt.title("User Logins by Day")
        plt.yticks(np.arange(0, 20, 1))
        plt.savefig('static/assets/loginHistory.png')
        plt.close()

        plt.bar(source_loans, loans_num, color='red')
        plt.yticks(np.arange(0, 10, 1))
        plt.xticks(rotation='vertical')
        plt.title("Source Loans by Serial Number")
        plt.savefig('static/assets/loanHistory.png')
        plt.close()

    except Exception:
        flash("Database error, unable to generate new reports")

    # Get all source loan histories
    source_histories = list(mongo.db.source_history.find())

    # Get the users first and last name and append to the source list to
    # avoid email being shown in the table
    for source_history in source_histories:
        if source_history["user"]:
            user = (mongo.db.users.find_one(
                {"email": source_history["user"]}))
            # Check that the user still exists
            if user:
                source_history.update({"first": user["first"]})
                source_history.update({"last": user["last"]})
            else:
                source_history.update({"first": ""})
                source_history.update({"last": ""})

    return render_template(
        "usageReport.html", name="usage plot",
        url1="static/assets/sourceUsed.png",
        url2="static/assets/loginHistory.png",
        url3="static/assets/loanHistory.png",
        source_histories=source_histories)

# -------------------------Source Request Management--------


@app.route("/approve_request", methods=["GET", "POST"])
def approve_request():
    #
    # Called when the admin user wants to see if there
    # are any new source requests to deal with
    #

    # Detect 404 page error
    if not session.get("user"):
        return render_template("404error.html")

    # Check if user has access to this page
    if (session["role"] == "user"):
        return render_template("errorPage.html")

    # Check for any requested but not approved sources
    if len(list(mongo.db.sources.find({"requested": "true"}))) == 0:
        showtable = "false"
        flash("You have no further source requests to approve")
    else:
        showtable = "true"

    existing_sources = list(mongo.db.sources.find({"requested": "true"}))

    # Get the users first and last name and append to
    # the source list to avoid email being shown in the table
    for source in existing_sources:
        if source["user"]:
            user = (mongo.db.users.find_one({"email": source["user"]}))
            # Check that the user still exists
            if user:
                source.update({"first": user["first"]})
                source.update({"last": user["last"]})
            else:
                source.update({"first": ""})
                source.update({"last": ""})

    return render_template(
        "approveRequest.html", sources=existing_sources, showtable=showtable)


@app.route("/approve_request_resp<source_serial_no>", methods=["GET", "POST"])
def approve_request_resp(source_serial_no):
    #
    # Called when an admin user clicks the button to approve
    # the use of a source
    #

    # Get mongodb record for source to be loaned
    existing_source = mongo.db.sources.find_one(
        {"serial_number": source_serial_no})

    # Create a source loan history entry document in mongodb
    outDate = datetime.today().strftime('%d-%m-%y')

    sourceLoan = {
        "serial_number": source_serial_no,
        "date_out": outDate,
        "date_in": "",
        "user": existing_source["user"],
        "laboratory": existing_source["laboratory"]
    }
    mongo.db.source_history.insert_one(sourceLoan)

    # Update the source document in mongodb
    submit = {"approved": "yes",
              "last_used": outDate}
    mongo.db.sources.find_one_and_update(
        {"serial_number": source_serial_no}, {'$set': submit})

    flash("Source Request Appoved")

    return approve_request()


@app.route("/return_source_resp<source_serial_no>", methods=["GET", "POST"])
def return_source_resp(source_serial_no):
    #
    # Called when an admin user returns a source to the inventory
    #

    inDate = datetime.today().strftime('%d-%m-%y')

    # Create update to the source_history document in mongodb with return date
    submit = {"date_in": inDate}

    # Find occurance of source serial number in source_history collection
    # with date_in empty date_in
    mongo.db.source_history.find_one_and_update(
        {"$and": [{"serial_number": source_serial_no},
         {"date_in": ""}]}, {'$set': submit})

    # Check if the source has been deleted from the inventory

    if mongo.db.sources.find_one({"serial_number": source_serial_no}):
        # Update the  source document in mongodb with
        # return date and removal approval status
        submit = {"last_used": inDate,
                  "approved": "no",
                  "requested": "false",
                  "user": ""
                  }
        mongo.db.sources.find_one_and_update(
            {"serial_number": source_serial_no}, {'$set': submit})

        flash("Source Returned To Inventory")
        return approve_request()
    else:
        flash("Source has been deleted from the inventory")
        return approve_request()


@app.route("/delete_source_resp/<source_serial_no>", methods=["GET", "POST"])
def delete_source_resp(source_serial_no):
    #
    # Called prior to user clicking button to delete a source
    # from the mongo db
    #

    # Detect 404 page error
    if not session.get("user"):
        return render_template("404error.html")

    # Check if user has access to this page
    if (session["role"] == "user"):
        return render_template("errorPage.html")

    existing_source = mongo.db.sources.find_one(
        {"serial_number": source_serial_no})
    used_times = mongo.db.source_history.count_documents(
        {"serial_number": source_serial_no})
    flash("Your are about to delete source: {}".format(source_serial_no))
    return render_template(
        "deleteSource.html",
        existing_source=existing_source,
        used_times=used_times)


# ----------------Create Read Update Delete User Accounts---


@app.route("/get_userb/<user_id>", methods=["GET", "POST"])
def get_userb(user_id):
    #
    # Called when an admin user approves a new account or suspends/re-approves
    # an account. User approved state starts at "appove" then toggles between
    # "approved" and "suspended"
    #

    # Detect 404 page error
    if not session.get("user"):
        return render_template("404error.html")

    # Check if user has access to this page
    if (session["role"] == "user"):
        return render_template("errorPage.html")

    existing_user = mongo.db.users.find_one({"_id": ObjectId(user_id)})

    # User cannot action his/her own account
    if existing_user["email"] == session["email"]:
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
        mongo.db.users.find_one_and_update(
            {"_id": ObjectId(user_id)}, {'$set': submit})

    users = list(mongo.db.users.find())
    return render_template("user.html", users=users)


@app.route("/get_userc/<user_id>", methods=["GET", "POST"])
def get_userc(user_id):
    #
    # Called when an admin user gives admin rights to another user
    #

    # Detect 404 page error
    if not session.get("user"):
        return render_template("404error.html")

    # Check if user has access to this page
    if (session["role"] == "user"):
        return render_template("errorPage.html")

    existing_user = mongo.db.users.find_one({"_id": ObjectId(user_id)})
    # Check existing user available
    if existing_user:
        # User cannot action his/her own account
        if existing_user["email"] == session["email"]:
            flash("You cannot action your own user account")
        else:
            # Admin user toggles another user account between admin/user roles
            if existing_user["role"] == "admin":
                submit = {"role": "user"}
            else:
                submit = {"role": "admin"}
            mongo.db.users.find_one_and_update(
                {"_id": ObjectId(user_id)}, {'$set': submit})
            flash("User role successfully updated")
        users = list(mongo.db.users.find())

    else:
        flash("Database error, user could not be given admin rights")

    return render_template("user.html", users=users)


@app.route("/get_userdelete/<user_id>", methods=["GET", "POST"])
def get_userdelete(user_id):
    #
    # Called when an admin user deletes a normal user account
    #

    # Detect 404 page error
    if not session.get("user"):
        return render_template("404error.html")

    # Check if user has access to this page
    if (session["role"] == "user"):
        return render_template("errorPage.html")

    existing_user = mongo.db.users.find_one({"_id": ObjectId(user_id)})

    # Check existing user available
    if existing_user:
        # User cannot delete his/her own account
        if existing_user["email"] == session["email"]:
            flash("You cannot delete your own user account")

        # Admin user cannot be deleted/removed
        elif existing_user["role"] == "admin":
            flash("You cannot delete an Admin user")

        # User account must be suspended before it can be deleted
        elif ((existing_user["approved"] == "approved") or
                (existing_user["approved"] == "approve")):
            flash("A user account must be suspended for it to be deleted")

        else:
            flash("Your are about to delete a user account.")
            return render_template(
                "userDelete.html", existing_user=existing_user)

    else:
        flash("User not found. Refer to admin user")

    users = list(mongo.db.users.find())
    return render_template("user.html", users=users)


@app.route("/delete_user_resp/<user_email>", methods=["GET", "POST"])
def delete_user_resp(user_email):
    #
    # Called to  confirm deletion of a user account from mongo db
    #

    # Detect 404 page error
    if not session.get("user"):
        return render_template("404error.html")

    # Check if user has access to this page
    if (session["role"] == "user"):
        return render_template("errorPage.html")

    # Check is user has a source on loan
    source_user = mongo.db.sources.find_one({"user": user_email})

    if source_user:
        # Get user name from user mongo db user collection
        user = mongo.db.users.find_one({"email": user_email})
        user_name = (
            user["first"]).capitalize() + " " + (user["last"]).capitalize()
        flash("User {} has sources on loan and cannot\
             be removed".format(user_name))

    else:
        mongo.db.users.delete_one({"email": user_email})
        flash("user account sucessfuly deleted")

    users = list(mongo.db.users.find())
    return render_template("user.html", users=users)


@app.route("/get_user")
def get_user():
    #
    # Called to display a complete table of all
    # users with either admin or user role
    #

    # Detect 404 page error
    if not session.get("user"):
        return render_template("404error.html")

    # Check if user has access to this page
    if (session["role"] == "user"):
        return render_template("errorPage.html")

    users = list(mongo.db.users.find())
    return render_template("user.html", users=users)

# -------------------------Create Read Update Delete Sources-----------------


@app.route("/get_sources")
def get_sources():
    #
    # Called when the full source inventory is to be read from mongo db
    # Calculates updated source activity
    #

    # Detect 404 page error
    if not session.get("user"):
        return render_template("404error.html")

    # Check if user has access to this page
    if (session["role"] == "user"):
        return render_template("errorPage.html")

    sources = list(mongo.db.sources.find())

    # Get the users first and last name and append to
    # the source list to avoid email being shown in the table
    for source in sources:
        if source["user"]:
            user = (mongo.db.users.find_one({"email": source["user"]}))
            # Check that the user still exists
            if user:
                source.update({"first": user["first"]})
                source.update({"last": user["last"]})
            else:
                source.update({"first": ""})
                source.update({"last": ""})

    for source in sources:
        # If db problem use existing activity
        try:
            serial_number = (source["serial_number"])
            origin_act = float(source["original_activity"])
            date_out = source["activation_date"]
            half_life = float(source["half_life"])

            # datetime.datetime.strptime only supported by date time
            # strftime used else where and requires
            # the datetime component from datetime
            import datetime
            delta_years = (((datetime.datetime.now(
            ) - datetime.datetime.strptime(date_out, '%d-%m-%y')).days)/365.25)
            from datetime import datetime

            # Calculate new activity using equation for radioactive decay
            new_act = str(
                round(origin_act*math.exp(
                    ((-1*math.log(2)*delta_years)/half_life)), 2))
        except Exception:
            # if calculation unsucessful use existing activity value
            new_act = origin_act

        source_new_act = {"activity_now": new_act}

        mongo.db.sources.find_one_and_update(
            {"serial_number": serial_number}, {'$set': source_new_act})

        return render_template("inventory.html", sources=sources)


@app.route("/add_source", methods=["GET", "POST"])
def add_source():
    #
    # Called when an admin user adds a new source to the source inventory
    #

    # Detect 404 page error
    if not session.get("user"):
        return render_template("404error.html")

    # Check if user has access to this page
    if (session["role"] == "user"):
        return render_template("errorPage.html")

    if request.method == "POST":
        # Get source from mongo db
        existing_source = mongo.db.sources.find_one(
            {"serial_number": request.form.get("serial_number")})

        # check if source serial number already exists in db
        if existing_source:
            flash("The source serial number already\
                exists, please select another")
        else:
            # Get isotope half life
            isotope_half_life = mongo.db.isotope_category.find_one(
                {"isotope": request.form.get("isotope")})

            # Create new source entry
            newSource = {
                "serial_number": request.form.get("serial_number").lower(),
                "department": request.form.get("department"),
                "laboratory": request.form.get("laboratory"),
                "location": request.form.get("location"),
                "isotope": request.form.get("isotope"),
                "half_life": isotope_half_life["halflife"],
                "half_life_units": "years",
                "original_activity": request.values.get(
                    "original_activity"),
                "original_activity_units": request.values.get(
                    "original_activity_units"),
                "activity_now": request.values.get("original_activity"),
                "activity_now_units": request.values.get(
                    "original_activity_units"),
                "activation_date": request.values.get("activation_date"),
                "security_group": request.values.get("security_group"),
                "type": request.values.get("encapsulation"),
                "last_used": "",
                "approved": "no",
                "requested": "false",
                "user": ""
            }
            mongo.db.sources.insert_one(newSource)
            flash("New source sucessfully added to inventory")

            sources = list(mongo.db.sources.find())
            return render_template("inventory.html", sources=sources)

    # No post setup html page for adding a new source
    security_codes = mongo.db.security_group.find()
    departments = mongo.db.departments.find()
    laboratories = mongo.db.laboratories.find()
    locations = mongo.db.locations.find()
    encapsulations = mongo.db.encapsulations.find()
    isotope_category = list(mongo.db.isotope_category.find())
    mode = "add"
    return render_template("addSource.html", security_codes=security_codes,
                           departments=departments,
                           laboratories=laboratories,
                           locations=locations,
                           mode=mode,
                           encapsulations=encapsulations,
                           isotope_category=isotope_category)


@app.route("/source_request", methods=["GET", "POST"])
def source_request():
    #
    # Called on selecting the SOURCE REQUEST option
    # Action open to users and admin
    #

    # Detect 404 page error
    if not session.get("user"):
        return render_template("404error.html")

    query = request.form.get("query")
    mode = "request"
    # Assume no sources found
    showsources = "false"
    sources = []
    if query:
        # Find collection of seached sources not already requested
        sources = list(mongo.db.sources.find(
            {"$and": [{"$text": {"$search": query}}, {"requested": "false"}]}))
        if sources:
            showsources = "true"
        else:
            flash("No matching sequences found.")
            sources = []

    return render_template(
        "sourceRequest.html",
        showsources=showsources,
        sources=sources, mode=mode)


@app.route("/del_source_req/<source_serial_no>", methods=["GET", "POST"])
def del_source_req(source_serial_no):
    #
    # Called when user deletes a source request before authorised by admin
    # Action open to users and admin
    #

    # Detect 404 page error
    if not session.get("user"):
        return render_template("404error.html")

    # Set up the source entry for avialable to use
    submit = {"approved": "no",
              "requested": "false",
              "user": ""}
    mongo.db.sources.find_one_and_update({"serial_number": source_serial_no},
                                         {'$set': submit})

    # Get list of sources held by the user
    # loanSources = list(mongo.db.sources.find({"user": session["email"]}))
    return redirect(url_for("userAccount"))


@app.route("/req_source_conf/<source_serial_no>", methods=["GET", "POST"])
def req_source_conf(source_serial_no):
    #
    # Action on clicking the REQUEST button on the SOURRCE REQUEST Page
    # Action open to users and admin
    #

    # Detect 404 page error
    if not session.get("user"):
        return render_template("404error.html")

    sources = list(mongo.db.sources.find_one(
        {"serial_number": source_serial_no}))

    # Update the source record
    submit = {"requested": "true", "user": session["email"]}
    mongo.db.sources.update_one(
        {"serial_number": source_serial_no}, {"$set": submit})

    flash("Source has been requested - please\
         wait for your request to be approved")

    showsources = "false"
    sources = ""
    mode = "request"
    return render_template(
        "sourceRequest.html",
        showsources=showsources,
        sources=sources,
        mode=mode)


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
            sources = list(mongo.db.sources.find(
                {"$text": {"$search": query}}))
            showsources = "true"
            return render_template(
                "sourceRequest.html",
                showsources=showsources,
                sources=sources,
                mode=mode)
        else:
            showsources = "false"
            sources = []
            return render_template(
                "sourceRequest.html",
                showsources=showsources,
                sources=sources,
                mode=mode)
    else:
        return render_template("errorPage.html")


@app.route("/update_source_activate", methods=["GET", "POST"])
def update_source_activate():
    #
    # Called when data relating to a source needs to updating in mongodb
    #

    if request.method == "POST":

        # Get source from mongo db
        existing_source = mongo.db.sources.find_one(
            {"serial_number": request.form.get("serial_number")})

        # check if source serial number already exists in db
        if existing_source:
            # Get isotope collection
            isotope = mongo.db.isotope_category.find_one(
                {"isotope": request.form.get("isotope")})

            # Check that isotope entry available in the collection
            if isotope:
                # Create updated source entry
                updateSource = {
                    "department": request.form.get("department"),
                    "laboratory": request.form.get("laboratory"),
                    "location": request.form.get("location"),
                    "isotope": request.form.get("isotope"),
                    "half_life": isotope["halflife"],
                    "half_life_units": "years",
                    "original_activity": request.values.get(
                        "original_activity"),
                    "original_activity_units": request.values.get(
                        "original_activity_units"),
                    "activity_now": request.values.get(
                        "original_activity"),
                    "activity_now_units": request.values.get(
                        "original_activity_units"),
                    "activation_date": request.values.get(
                        "activation_date"),
                    "security_group": request.values.get(
                        "security_group"),
                    "type": request.values.get("encapsulation")
                }

                mongo.db.sources.find_one_and_update(
                    {"serial_number": request.form.get(
                        "serial_number")}, {'$set': updateSource})

                flash("The source data has been sucessfully updated")
            else:
                # Do not update the source entry
                flash("Database error source data\
                     has not been updated. Refer to admin user.")
        else:
            flash("Database error source data\
                 has not been updated. Refer to admin user.")

        return redirect(url_for("get_sources"))


@ app.route("/update_source_resp/<source_serial_no>", methods=["GET", "POST"])
def update_source_resp(source_serial_no):
    #
    # Called when data relating to a source requires update
    #

    # Detect 404 page error
    if not session.get("user"):
        return render_template("404error.html")

    # Check if user has access to this page
    if (session["role"] == "user"):
        return render_template("errorPage.html")

    existing_source = (mongo.db.sources.find_one(
        {"serial_number": source_serial_no}))
    security_codes = (mongo.db.security_group.find())
    departments = (mongo.db.departments.find())
    laboratories = (mongo.db.laboratories.find())
    locations = (mongo.db.locations.find())
    encapsulations = (mongo.db.encapsulations.find())

    return render_template(
        "updateSource.html",
        existing_source=existing_source,
        security_codes=security_codes,
        departments=departments,
        locations=locations,
        laboratories=laboratories,
        encapsulations=encapsulations)


@ app.route("/delete_source", methods=["GET", "POST"])
def delete_source():
    #
    # called when the admin user selects a source for deletion via a query
    #

    # Detect 404 page error
    if not session.get("user"):
        return render_template("404error.html")

    # Check if user has access to this page
    if (session["role"] == "user"):
        return render_template("errorPage.html")

    query = request.form.get("query")
    mode = "delete"
    if query:
        # line of code from Code Institute
        # tuition Data "Centric Design Mini Project"
        sources = list(mongo.db.sources.find(
            {"$text": {"$search": query}}))
        showsources = "true"
        return render_template(
            "sourceRequest.html",
            showsources=showsources,
            sources=sources,
            mode=mode)
    else:
        showsources = "false"
        sources = []
        return render_template(
            "sourceRequest.html",
            showsources=showsources,
            sources=sources,
            mode=mode)


@ app.route("/del_source_conf/<source_serial_no>", methods=["GET", "POST"])
def del_source_conf(source_serial_no):
    #
    # Gets source data from the mongo db and generates a table
    #

    # Detect 404 page error
    if not session.get("user"):
        return render_template("404error.html")

    # Check if user has access to this page
    if (session["role"] == "user"):
        return render_template("errorPage.html")

    # Find if there is a current user of the source
    existing_source = mongo.db.sources.find_one(
        {"serial_number": source_serial_no})
    existing_source_user = existing_source["user"]

    if existing_source_user:
        flash("Source: {} is on loan and could not be deleted ".format(
            source_serial_no))
    else:
        # Go ahead and delete
        mongo.db.sources.delete_one({"serial_number": source_serial_no})
        flash("Source: {} has been deleted".format(source_serial_no))

    return redirect(url_for("get_sources"))


@ app.route("/userAccount", methods=["GET", "POST"])
def userAccount():
    #
    # User or admin users profile page
    #

    # Detect 404 page error
    if not session.get("user"):
        return render_template("404error.html")

    # User already logged in so use session cookie as key to user details
    existing_user = mongo.db.users.find_one({"email": session["email"]})
    user_id = existing_user["_id"]

    if request.method == "POST":
        if request.form.get("password") != request.form.get("repeat_password"):
            flash("Please ensure that that your password entries match")
        else:
            # Construct user profile update payload but ensure inputs not blank
            submit = {}
            if request.form.get("password") != "":
                submit.update({"password": generate_password_hash(
                    request.form.get("password"))})
            if request.form.get("department") != "":
                submit.update({"department": request.form.get("department")})
            if request.form.get("research_group") != "":
                submit.update(
                    {"research_group": request.form.get("research_group")})

            mongo.db.users.find_one_and_update(
                {"_id": ObjectId(user_id)}, {'$set': submit})

            flash("Your account details have been successfully updated")

    existing_user = mongo.db.users.find_one({"_id": ObjectId(user_id)})

    # Get list of sources held by the user
    loanSources = list(mongo.db.sources.find({"user": session["email"]}))
    departments = list(mongo.db.departments.find())

    if len(loanSources) == 0:
        showtable = "false"
    else:
        showtable = "true"

    return render_template(
        "userAccount.html",
        user=existing_user,
        usersources=loanSources,
        departments=departments,
        showtable=showtable)


# -------------------------Manage isotope types------------------------
@app.route("/manage_isotopes", methods=["GET", "POST"])
def manage_isotopes():
    #
    #  Called to list out isotope types to the admin user
    #

    # Detect 404 page error
    if not session.get("user"):
        return render_template("404error.html")

    # Check if user has access to this page
    if (session["role"] == "user"):
        return render_template("errorPage.html")

    if request.method == "POST":
        existing_isotope = mongo.db.isotope_category.find_one(
            {"isotope": request.form.get("isotope")})
        if existing_isotope:
            flash("Duplicated entry, please try again")
        else:
            isotope_entry = {
                "isotope": request.form.get("isotope"),
                "halflife": request.form.get("halflife")
            }
            mongo.db.isotope_category.insert_one(isotope_entry)

    isotopes = list(mongo.db.isotope_category.find())
    return render_template("isotopeTypes.html", isotopes=isotopes)


@app.route("/delete_isotope/<isotope>", methods=["GET", "POST"])
def delete_isotope(isotope):
    #
    # Called to  confirm deletion of an isotope from the list in mongo db
    #

    # Detect 404 page error
    if not session.get("user"):
        return render_template("404error.html")

    # Check if user has access to this page
    if (session["role"] == "user"):
        return render_template("errorPage.html")

    existing_isotope = mongo.db.isotope_category.find_one(
        {"isotope": isotope})
    flash("Your are about to delete isotope: {}".format(isotope))
    return render_template(
        "isotopeDelete.html", existing_isotope=existing_isotope)


@app.route("/delete_isotope_resp/<isotope>", methods=["GET", "POST"])
def delete_isotope_resp(isotope):
    #
    # Called to  confirm deletion of an isotope from the list in mongo db
    #

    # Do not delete source is still on loan
    sources = list(mongo.db.sources.find(
        {"$and": [{"$or": [
            {"approved": "yes"}, {"requested": "true"}]},
            {"isotope": isotope}]}))

    if sources:
        flash("Isotope {} is still on loan and\
             cannot be deleted".format(isotope))
    else:
        mongo.db.isotope_category.delete_one({"isotope": isotope})

    return redirect(url_for("manage_isotopes"))


@app.route("/update_isotope/<isotope>", methods=["GET", "POST"])
def update_isotope(isotope):
    #
    # Called to update an isotope type in the isotope_category collection and
    # to update all references to the isotope in the source collection
    #

    # Detect 404 page error
    if not session.get("user"):
        return render_template("404error.html")

    # Check if user has access to this page
    if (session["role"] == "user"):
        return render_template("errorPage.html")

    # Get isotope list and display
    existing_isotope = mongo.db.isotope_category.find_one(
        {"isotope": isotope})
    return render_template(
        "isotopeUpdate.html", existing_isotope=existing_isotope)


@app.route("/isotopes_update_conf/<isotope_id>", methods=["GET", "POST"])
def isotopes_update_conf(isotope_id):
    #
    #  Called to list out isotope types to the admin user
    #

    # Detect 404 page error
    if not session.get("user"):
        return render_template("404error.html")

    # Check if user has access to this page
    if (session["role"] == "user"):
        return render_template("errorPage.html")

    if request.method == "POST":
        # Do not delete source is still on loan
        existing_source = list(mongo.db.sources.find(
            {"$and": [{"approved": "yes"},
             {"isotope": request.form.get("isotope")}]}))
        if existing_source:
            flash("Isotope {} is still on loan and \
                cannot be updated".format(isotope_id))
        else:
            isotope_update = {
                "isotope": request.form.get("isotope"),
                "halflife": request.form.get("halflife")
            }

            # Update the source inventory (db collection)
            existing_isotope = mongo.db.isotope_category.find_one(
                {"_id": ObjectId(isotope_id)})
            mongo.db.sources.update_many(
                {"isotope": existing_isotope["isotope"]},
                {'$set': isotope_update})

            # Update the db colection of isotope categories
            mongo.db.isotope_category.find_one_and_update(
                {"_id": ObjectId(isotope_id)}, {'$set': isotope_update})
            flash("Isotope type sucessfully updated")

    isotopes = list(mongo.db.isotope_category.find())
    return render_template("isotopeTypes.html", isotopes=isotopes)

# -----------------Error Handlers & Dummy hrefs--------------------------


@app.errorhandler(404)
def invalid_route(e):
    #
    # Handles 404 page not found error
    # Guidance from
    # https://flask.palletsprojects.com/en/1.1.x/patterns/errorpages/

    return render_template("404error.html")


@app.route("/faculty_link", methods=["GET", "POST"])
def faculty_link():
    #
    # Handles href to dummy Physics faculty web site
    #

    return render_template("physicsFaculty.html")


# -------------------------Main Loop-----------------------------------
if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
            port=int(os.environ.get("PORT")),
            debug=True)
