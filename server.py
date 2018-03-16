from flask import Flask, request, redirect, render_template, session, flash
import re
from mysqlconnection import MySQLConnector
email_regex = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
app = Flask(__name__)
app.secret_key = 'HereIsMySecret...'
mysql = MySQLConnector(app, 'email_validation')
@app.route("/")
def index():
    return render_template("index.html")
@app.route("/", methods=["post"])
def index1():
    err = False
    if len(request.form["email_address"]) < 1:
        flash("no dummy. you have to enter an email adress.")
        err = True
    elif not email_regex.match(request.form["email_address"]):  
        flash("invalid email address")
        err = True
    if err == True:
        return redirect("/")
    query = "INSERT INTO customer (email_address, date_created) VALUES (:email_address, NOW())"
    data = {
        "email_address": request.form["email_address"],
    }
    mysql.query_db(query,data)
    return redirect("/success")
@app.route("/success")
def success():
    flash("The email address you entered {} is a VALID email address! Thank you!")
    query = "select customer.email_address, customer.date_created, date_format(customer.date_created, '%b %d %Y %h %i') AS date FROM customer"
    cust = mysql.query_db(query)
    return render_template('success.html', cust=cust)
app.run(debug=True)
