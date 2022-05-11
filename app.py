from crypt import methods
from datetime import timedelta
import email
import json
from sqlalchemy import or_,and_
import re
from flask import after_this_request, jsonify, render_template,request, request_started,url_for,redirect,session
from types import MethodDescriptorType
from flask.helpers import flash
from flask_migrate import Migrate, migrate
from models import *
from flask_script import Manager
import psycopg2
from datetime import datetime as date
import uuid
# from flask_login import login_user,logout_user
import random
import string
import secrets # import package 
from flask_mail import Message,Mail
# from generatereports import *
from config import * 
from PIL import Image
import os
from werkzeug.utils import secure_filename 

con = psycopg2.connect(database="carmanagement", user="kalabai", password="kalabai", host="127.0.0.1", port="5432")
cursor = con.cursor()



POSTGRES={
    'user':'kalabai',
    'pw':'kalabai',
    'host':'localhost',
    'port':'5432',
    'db':'carmanagement'
}
db.init_app(app)
migrate=Migrate(app,db)
app.config['SQLALCHEMY_DATABASE_URI']='postgresql://%(user)s:%(pw)s@%(host)s:%(port)s/%(db)s' %POSTGRES
app.config.update(
    DEBBUG=True,
    MAIL_SERVER=("smtp.gmail.com"),
    MAIL_PORT=465,
    MAIL_USE_SSL=True,
    MAIL_USE_TLS=False,
    MAIL_USERNAME="manukalabai214@gmail.com",
    MAIL_PASSWORD="Compscience1"
)
mail=Mail(app)


@app.route("/")
def home():
    return render_template("homepage.html")


@app.route("/customer_registration",methods=["POST","GET"])
def customer():
    if request.method=="POST":
        user=customer_registration.query.all()
        if(customer_registration.query.filter(customer_registration.username == request.form['username'])).first():
            flash('The user already exists')
            return redirect(url_for('customer'))
        onetime=10
        res = ''.join(secrets.choice(string.ascii_letters + string.digits) for x in range(onetime)) 
        print("your one time password is  :"+ str(res)) 
        msg=Message("first time password",
        sender="manukalabai214@gmail.com",
        body="your one time password is "+res ,
        recipients=[request.form["email"]])       
        mail.send(msg)

        newuser=customer_registration(username=request.form['username'],password=res,email=request.form['email'],id_number=request.form['id_number'],phone_number=request.form['phone_number'],first_name=request.form['first_name'],last_name=request.form['last_name'],gender=request.form['gender'])
        newuser.save()
        flash('you have successfully registered')

        return render_template("customer/customer_register.html")
    return render_template("customer/customer_register.html")

@app.route("/admin_registration",methods=["POST","GET"])
def admin():
    if request.method=="POST":
        admin=admin_registration.query.all()
        if(admin_registration.query.filter(admin_registration.username == request.form['username'])).first():
            flash('The user with the username already exists')
            return redirect(url_for('admin'))
        onetime=10
        res = ''.join(secrets.choice(string.ascii_letters + string.digits) for x in range(onetime)) 
        print("your one time password is  :"+ str(res)) 
        msg=Message("first time password",
        sender="manukalabai214@gmail.com",
        body="your one time password is "+res ,
        recipients=[request.form["email"]])       
        mail.send(msg)

        newadmin=admin_registration(username=request.form['username'],password=res,email=request.form['email'],id_number=request.form['id_number'],phone_number=request.form['phone_number'],first_name=request.form['first_name'],last_name=request.form['last_name'],gender=request.form['gender'],role=request.form['role'])
        newadmin.save()
        flash('please check in your email to get your password,use the password to login','success')

        return render_template("admin/admin_register.html")
    return render_template("admin/admin_register.html")

@app.route("/superadmin_registration",methods=["POST","GET"])
def superadmin():
    if request.method=="POST":
        superadmin=superadmin_registration.query.all()
        if(superadmin_registration.query.filter(superadmin_registration.username == request.form['username'])).first():
            flash('The user with the username already exists')
            return redirect(url_for('superadmin'))
        onetime=10
        res = ''.join(secrets.choice(string.ascii_letters + string.digits) for x in range(onetime)) 
        print("your one time password is  :"+ str(res)) 
        msg=Message("first time password",
        sender="manukalabai214@gmail.com",
        body="your one time password is "+res ,
        recipients=[request.form["email"]])       
        mail.send(msg)

        newsuperadmin=superadmin_registration(username=request.form['username'],password=res,email=request.form['email'],id_number=request.form['id_number'],phone_number=request.form['phone_number'],first_name=request.form['first_name'],last_name=request.form['last_name'],gender=request.form['gender'],role=request.form['role'])
        newsuperadmin.save()
        flash('please check in your email to get your password,use the password to login','success')

        return render_template("superadmin/superadmin_register.html")
    return render_template("superadmin/superadmin_register.html")


@app.route("/manager_registration",methods=["POST","GET"])
def manager():
    if request.method=="POST":
        manager=manager_registration.query.all()
        if(manager_registration.query.filter(manager_registration.username == request.form['username'])).first():
            flash('The user with the username already exists')
            return redirect(url_for('manager'))
        onetime=10
        res = ''.join(secrets.choice(string.ascii_letters + string.digits) for x in range(onetime)) 
        print("your one time password is  :"+ str(res)) 
        msg=Message("first time password",
        sender="manukalabai214@gmail.com",
        body="your one time password is "+res ,
        recipients=[request.form["email"]])       
        mail.send(msg)

        newmanager=manager_registration(username=request.form['username'],password=res,email=request.form['email'],id_number=request.form['id_number'],phone_number=request.form['phone_number'],first_name=request.form['first_name'],last_name=request.form['last_name'],gender=request.form['gender'],role=request.form['role'])
        newmanager.save()
        flash('please check in your email to get your password,use the password to login','success')

        return render_template("manager/manager_register.html")
    return render_template("manager/manager_register.html")

@app.route("/customer_login",methods=["POST","GET"])
def customer_login():
    if 'user' in session:
        user=customer_registration.query.filter(customer_registration.username==session['user']).first()
        return render_template("customer/customer_dashboard.html",user=user)
    elif request.method=="POST":

        user=customer_registration.query.filter(customer_registration.username==request.form['username']).first()
        if user:
            if sha256_crypt.verify(request.form['password'],user.password):
                session['user']=request.form['username']
                return render_template("customer/customer_dashboard.html",user=user)                
    return render_template("customer/customer_login.html")



@app.route("/admin_login",methods=["POST","GET"])
def admin_login():
    if 'admin' in session:
        admin=admin_registration.query.filter(admin_registration.username==session['admin']).first()
        return render_template("admin/admin_dashboard.html",admin=admin)
    elif request.method=="POST":

        admin=admin_registration.query.filter(admin_registration.username==request.form['username']).first()
        if admin:
            if sha256_crypt.verify(request.form['password'],admin.password):
                session['admin']=request.form['username']
                return render_template("admin/admin_dashboard.html",admin=admin)                
    return render_template("admin/admin_login.html")

@app.route("/superadmin_login",methods=["POST","GET"])
def superadmin_login():
    if "superadmin" in session:
        return render_template("superadmin/superadmin_dashboard.html")

    if request.method=="POST":
        superadmin=superadmin_registration.query.filter(superadmin_registration.username==request.form['username']).first()
        if superadmin:
            if sha256_crypt.verify(request.form['password'],superadmin.password):
                session['superadmin']=request.form['username']
                return render_template("superadmin/superadmin_dashboard.html")
    return render_template("superadmin/superadmin_login.html")

@app.route("/manager_login",methods=["POST","GET"])
def manager_login():
    if request.method=="POST":
        manager=manager_registration.query.filter(manager_registration.username==request.form['username']).first()
        if manager:
            if sha256_crypt.verify(request.form['password'],manager.password):
                session['manager']=request.form['username']
                return render_template("manager/manager_dashboard.html")
    return render_template("manager/manager_login.html")



@app.route("/changepassword",methods=["POST","GET"])
def changepassword():
    if request.method=="POST":
        if "superadmin" in session:
            superadmin = superadmin_registration.query.filter(superadmin_registration.username==session['superadmin']).first()
            if not request.form['old_password'] or not request.form['new_password'] or not request.form['confirm_password']:                
                flash("fill in all the details")
            elif not request.form['new_password'] == request.form['confirm_password']:
                flash("the new password and confirmed passwords don't match")
            elif not sha256_crypt.verify(request.form['old_password'],superadmin.password):
                flash(" please enter the correct old password")
                return redirect(url_for("changepassword"))
            else:
                superadmin.password= sha256_crypt.encrypt(request.form['new_password'])
                superadmin.save()
                flash("password changed successfully")
                return render_template("superadmin/superadmin_dashboard.html")
            
@app.route("/upadatepassword",methods=["POST","GET"])
def updatepassword():
    if request.method=="POST":
        if "user" in session:
            user = customer_registration.query.filter(customer_registration.username==session['user']).first()
            if not request.form['old_password'] or not request.form['new_password'] or not request.form['confirm_password']:                
                flash("fill in all the details")
            elif not request.form['new_password'] == request.form['confirm_password']:
                flash("the new password and confirmed passwords don't match")
            elif not sha256_crypt.verify(request.form['old_password'],user.password):
                flash(" please enter the correct old password")
                return redirect(url_for("updatepassword"))
            else:
                user.password= sha256_crypt.encrypt(request.form['new_password'])
                user.save()
                flash("password changed successfully")
                return redirect(url_for('customer_login'))

@app.route("/chanagepassworda",methods=["POST","GET"])
def changepassworda():
    if request.method=="POST":
        if "admin" in session:
            admin = admin_registration.query.filter(admin_registration.username==session['admin']).first()
            if not request.form['old_password'] or not request.form['new_password'] or not request.form['confirm_password']:                
                flash("fill in all the details")
            elif not request.form['new_password'] == request.form['confirm_password']:
                flash("the new password and confirmed passwords don't match")
            elif not sha256_crypt.verify(request.form['old_password'],admin.password):
                flash(" please enter the correct old password")
                return redirect(url_for("changepassworda"))
            else:
                admin.password= sha256_crypt.encrypt(request.form['new_password'])
                admin.save()
                flash("password changed successfully")
                return render_template("admin/admin_dashboard.html")


@app.route("/viewadmins", methods=["POST", "GET"])
def viewadmins():
    admin = admin_registration.query.all()
    return render_template("superadmin/view_admins.html", admin=admin)

@app.route("/viewcustomers", methods=["POST", "GET"])
def viewcustomers():
    user = customer_registration.query.all()
    return render_template("superadmin/view_customers.html", user=user)


@app.route("/update_customer_details",methods=["POST","GET"])
def update():
    if request.method=="POST":
        if "user" in session:
            user = customer_registration.query.filter(customer_registration.username==session["user"]).first()

            user.first_name = request.form['first_name']
            user.last_name = request.form['last_name']
            user.username = request.form['username']
            user.email = request.form['email']
            user.phone_number = request.form['phone_number']
            user.id_number = request.form['id_number']
            user.save()
            flash("details updated successfully")
    return redirect(url_for("customer_login"))


@app.route("/update_admin_details",methods=["POST","GET"])
def updatedetails():
    if request.method=="POST":
        if "admin" in session:
            admin = admin_registration.query.filter(admin_registration.username==session["admin"]).first()

            admin.first_name = request.form['first_name']
            admin.last_name = request.form['last_name']
            admin.username = request.form['username']
            admin.email = request.form['email']
            admin.phone_number = request.form['phone_number']
            admin.id_number = request.form['id_number']
            admin.save()
            flash("details updated successfully")
    return redirect(url_for("admin_login"))

@app.route("/updateadm",methods=["POST","GET"])
def updateadm():
    if request.method=="POST":
        if "superadmin" in session:
            admin = admin_registration.query.filter(admin_registration.username==request.form['username']).first()
            admin.first_name = request.form['first_name']
            admin.last_name = request.form['last_name']
            # admin.username = request.form['username']
            admin.email = request.form['email']
            # admin.phone_number = request.form['phone_number']
            # admin.id_number = request.form['id_number']
            admin.role = request.form['role']
            admin.gender = request.form['gender']
            admin.save()
            flash("details updated successfully")
            return redirect(url_for("superadmin_login"))


@app.route("/serializedadmins")
def serializedadmins():
    @after_this_request
    def add_header(response):
        response.headers.add("Access-Control-Allow-Origin",'*')
        return response
    admin=admin_registration.query.all()
    newadmin=json.dumps([a.serialize() for a in admin])
    return jsonify(newadmin)


@app.route('/search_admin',methods=["POST","GET"])
def search_admin():
    if request.method == "POST":
        admin=admin_registration.query.filter(or_(admin_registration.first_name==request.form['search'],admin_registration.last_name==request.form['search'],admin_registration.email==request.form['search'],admin_registration.username==request.form['search'],admin_registration.gender==request.form['search']))
        return render_template("superadmin/searchadmin.html", admin=admin)

@app.route("/addcar",methods=["POST","GET"])
def addcar():
    if request.method == "POST":
        file=request.files['file']
        image = Image.open(file)
        new_image = image.resize((500,500))
        filename = secure_filename(file.filename)
        new_image.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        #  code to addcar
        car=add_car.query.all()
        if add_car.query.filter(add_car.number_plate == request.form['number_plate']).first():
            flash('The car has already been added')
            return redirect(url_for('addcar'))
        newcar=add_car(number_plate=request.form['number_plate'],model=request.form['model'],capacity=request.form['capacity'],gear=request.form['gear'],no_of_cars=request.form['no_of_cars'],logbook_number=request.form['logbook_number'],origin=request.form['origin'],brand=request.form['brand'],price=request.form['price'],engine=request.form['engine'],image=filename)
        newcar.save()
        flash("The car has been added successfully") 
        return render_template("admin/add_new_car.html")             
    return render_template("admin/add_new_car.html") 

    if request.method == "GET":        
        return render_template("admin/add_new_car.html")
    

@app.route('/logout')
def logout():
    if 'user' in session:
        session.pop('user', None)
        return redirect(url_for("home"))
    elif "admin" in session:
        session.pop("admin",None)
        return redirect(url_for("home"))
    elif 'superadmin' in session:
        session.pop('superadmin', None)
        return redirect(url_for("home"))
    else:
        session.pop('manager', None)
        return redirect(url_for("home"))