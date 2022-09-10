from crypt import methods
from datetime import timedelta
import email
import json
from urllib import response

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

from reports import *

con = psycopg2.connect(database="carmanagement", user="kalabai", password="kalabai", host="127.0.0.1", port="5432")
cursor = con.cursor()



POSTGRES={
    'user':'kalabai',
    'pw':'kalabai',
    'host':'localhost',
    'port':'5432',
    'db':'carmanagement'
}
app.config['SQLALCHEMY_DATABASE_URI']='postgresql://%(user)s:%(pw)s@%(host)s:%(port)s/%(db)s' %POSTGRES
db.init_app(app)
migrate=Migrate(app,db)

app.config.update(
    DEBBUG=True,
    MAIL_SERVER=("smtp.gmail.com"),
    MAIL_PORT=465,
    MAIL_USE_SSL=True,
    MAIL_USE_TLS=False,
    MAIL_USERNAME="manukalabai214@gmail.com",
    MAIL_PASSWORD="kxclhdefkqbrlcra"
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

def send_mail(subject, recipients,body):
    msg=Message(subject,
    sender="manukalabai214@gmail.com",
    body=body ,
    recipients=recipients)      
    mail.send(msg)


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
            flash('The user with the username already exists','error')
            return redirect(url_for('manager'))
        onetime=10
        res = ''.join(secrets.choice(string.ascii_letters + string.digits) for x in range(onetime)) 
        print("your one time password is  :"+ str(res)) 
        msg=Message("first time password",
        sender="manukalabai214@gmail.com",
        body="your one time password is "+res ,
        recipients=[request.form["email"]])       
        mail.send(msg)

        newmanager=manager_registration(username=request.form['username'],password=res,email=request.form['email'],id_number=request.form['id_number'],phone_number=request.form['phone_number'],first_name=request.form['first_name'],last_name=request.form['last_name'],staff_id=request.form['staff_id'],gender=request.form['gender'],role=request.form['role'])
        newmanager.save()
        flash('please check in your email to get your password,use the password to login','success')

        return render_template("manager/manager_register.html")
    return render_template("manager/manager_register.html")

@app.route("/customer_login",methods=["POST","GET"])
def customer_login():
    if 'user' in session:
        user=customer_registration.query.filter(customer_registration.username==session['user']).first()
        cartitems = cart_table.query.filter(cart_table.username==session['user']).count()
        # bkappointment=book_appointment(appointment_id=uuid.uuid4(),number_plate=request.form['number_plate'],username=session['user'],email=request.form['email'],date=request.form['date'],location=request.form['location'],description=request.form['description']).count()
        return render_template("customer/customer_dashboard.html",user=user,cartitems=cartitems)
    elif request.method=="POST":

        user=customer_registration.query.filter(customer_registration.username==request.form['username']).first()
        if user:
            if sha256_crypt.verify(request.form['password'],user.password):
                session['user']=request.form['username']
                cartitems = cart_table.query.filter(cart_table.username==session['user']).count()
                return render_template("customer/customer_dashboard.html",user=user,cartitems=cartitems)                
    return render_template("customer/customer_login.html")



@app.route("/admin_login",methods=["POST","GET"])
def admin_login():
    bkappointment=book_appointment.query.count()

    if 'admin' in session:
        admin=admin_registration.query.filter(admin_registration.username==session['admin']).first()
        return render_template("admin/admin_dashboard.html",admin=admin,bkappointment=bkappointment)
    elif request.method=="POST":

        admin=admin_registration.query.filter(admin_registration.username==request.form['username']).first()
        if admin:
            if sha256_crypt.verify(request.form['password'],admin.password):
                session['admin']=request.form['username']
                return render_template("admin/admin_dashboard.html",admin=admin,bkappointment=bkappointment)                
    return render_template("admin/admin_login.html")

@app.route("/superadmin_login",methods=["POST","GET"])
def superadmin_login():
    if "superadmin" in session:
        superadmin=superadmin_registration.query.filter(superadmin_registration.username==session['superadmin']).first()
        return render_template("superadmin/superadmin_dashboard.html")

    elif request.method=="POST":
        superadmin=superadmin_registration.query.filter(superadmin_registration.username==request.form['username']).first()
        if superadmin:
            if sha256_crypt.verify(request.form['password'],superadmin.password):
                session['superadmin']=request.form['username']
                return render_template("superadmin/superadmin_dashboard.html")
    return render_template("superadmin/superadmin_login.html")

@app.route("/manager_login",methods=["POST","GET"])
def manager_login():
    if 'manager' in session:
        manager=manager_registration.query.filter(manager_registration.username==session['manager']).first()
        return render_template("manager/manager_dashboard.html",manager=manager)

    elif request.method=="POST":
        manager=manager_registration.query.filter(manager_registration.username==request.form['username']).first()
        if manager:
            if sha256_crypt.verify(request.form['password'],manager.password):
                session['manager']=request.form['username']
                return render_template("manager/manager_dashboard.html",manager=manager)
    return render_template("manager/manager_login.html")



@app.route("/changepassword",methods=["POST","GET"])
def changepassword():
    if request.method=="POST":
        if "superadmin" in session:
            superadmin = superadmin_registration.query.filter(superadmin_registration.username==session['superadmin']).first()
            if not request.form['old_password'] or not request.form['new_password'] or not request.form['confirm_password']:                
                flash("fill in all the details")
            elif not request.form['new_password'] == request.form['confirm_password']:
                flash("the new password and confirmed passwords don't match", 'error')
            elif not sha256_crypt.verify(request.form['old_password'],superadmin.password):
                flash(" please enter the correct old password", 'error')
                return redirect(url_for("changepassword"))
            else:
                superadmin.password= sha256_crypt.encrypt(request.form['new_password'])
                superadmin.save()
                flash("password changed successfully",'success')
                return render_template("superadmin/superadmin_dashboard.html")
            
@app.route("/upadatepassword",methods=["POST","GET"])
def updatepassword():
    if request.method=="POST":
        if "user" in session:
            user = customer_registration.query.filter(customer_registration.username==session['user']).first()
            if not request.form['old_password'] or not request.form['new_password'] or not request.form['confirm_password']:                
                flash("fill in all the details", 'error')
            elif not request.form['new_password'] == request.form['confirm_password']:
                flash("the new password and confirmed passwords don't match", 'error')
            elif not sha256_crypt.verify(request.form['old_password'],user.password):
                flash(" please enter the correct old password", 'error')
                return redirect(url_for("updatepassword"))
            else:
                user.password= sha256_crypt.encrypt(request.form['new_password'])
                user.save()
                flash("password changed successfully", 'success')
                return redirect(url_for('customer_login'))

@app.route("/chanagepassworda",methods=["POST","GET"])
def changepassworda():
    if request.method=="POST":
        if "admin" in session:
            admin = admin_registration.query.filter(admin_registration.username==session['admin']).first()
            if not request.form['old_password'] or not request.form['new_password'] or not request.form['confirm_password']:                
                flash("fill in all the details", 'error')
            elif not request.form['new_password'] == request.form['confirm_password']:
                flash("the new password and confirmed passwords don't match", 'error')
            elif not sha256_crypt.verify(request.form['old_password'],admin.password):
                flash(" please enter the correct old password" ,'error')
                return redirect(url_for("changepassworda"))
            else:
                admin.password= sha256_crypt.encrypt(request.form['new_password'])
                admin.save()
                flash("password changed successfully", 'success')
            return redirect(url_for('admin_login'))

@app.route("/chanagepasswordbymanager",methods=["POST","GET"])
def changepasswordbymanager():
    if request.method=="POST":
        if "manager" in session:
            manager = manager_registration.query.filter(manager_registration.username==session['manager']).first()
            if not request.form['old_password'] or not request.form['new_password'] or not request.form['confirm_password']:                
                flash("fill in all the details", 'error')
            elif not request.form['new_password'] == request.form['confirm_password']:
                flash("the new password and confirmed passwords don't match", 'error')
            elif not sha256_crypt.verify(request.form['old_password'],manager.password):
                flash(" please enter the correct old password" ,'error')
                # return redirect(url_for("changepassworda"))
            else:
                manager.password= sha256_crypt.encrypt(request.form['new_password'])
                manager.save()
                flash("password changed successfully", 'success')
            return redirect(url_for('manager_login'))


@app.route("/viewadmins", methods=["POST", "GET"])
def viewadmins():
    admin = admin_registration.query.all()
    return render_template("superadmin/view_admins.html", admin=admin)

@app.route("/viewcustomers", methods=["POST", "GET"])
def viewcustomers():
    user = customer_registration.query.all()
    return render_template("superadmin/view_customers.html", user=user)


@app.route("/selectcartobeviewed", methods=["POST", "GET"])
def selectcartobeviewed():
    car = add_car.query.all()
    return render_template("customer/select_car_to_be_viewed.html", car=car)

@app.route("/viewcars", methods=["POST", "GET"])
def viewcars():
    car = add_car.query.all()
    cartitems=[]
    if 'user' in session:
        cartitems = cart_table.query.filter(cart_table.username==session['user']).count()
    return render_template("customer/view_cars.html", car=car,cartitems=cartitems)

@app.route("/viewcars2", methods=["POST", "GET"])
def viewcars2():
        car = add_car.query.filter(add_car.number_plate==request.args.get('number_plate')).first()
        cartitems=[]
        if 'user' in session:
            cartitems = cart_table.query.filter(cart_table.username==session['user']).count()
        return render_template("customer/view_cars2.html", car=car,cartitems=cartitems)

# @app.route("/viewcars3", methods=["POST", "GET"])
# def viewcars3():
#         car = add_car.query.filter(add_car.number_plate==request.args.get('number_plate')).first()
#         return render_template("customer/view_cars3.html", car=car)


@app.route("/selectreport",methods=["GET","POST"])
def selectreport():
    if request.method=="POST":
        return redirect(url_for("selectreport"))

@app.route("/viewcartobesold", methods=["POST", "GET"])
def viewcarstobesold():
    car=add_car.query.filter(add_car.purpose==request.args.get('filter')).all()
    cartitems=[]
    if 'user' in session:
     cartitems = cart_table.query.filter(cart_table.username==session['user']).count()
    
    return render_template("customer/view_cars.html", car=car, cartitems=cartitems)

@app.route("/viewcartobehired", methods=["POST", "GET"])
def viewcarstobehired():
    car=add_car.query.filter(add_car.purpose==request.args.get('filter')).all()
    return render_template("customer/view_cars.html", car=car)



@app.route("/viewcarsbyadmin", methods=["POST","GET"])
def viewcarsbyadmin():
    admin=admin_registration.query.filter(admin_registration.username==session['admin']) 
    car = add_car.query.all()
    return render_template("admin/view_cars_by_admin.html", car=car,admin=admin)

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
            flash("details updated successfully","success")
    return redirect(url_for("customer_login"))

@app.route("/update_manager_details",methods=["POST","GET"])
def update_manager_details():
    if request.method=="POST":
        if "manager" in session:
            manager = manager_registration.query.filter(manager_registration.username==session["manager"]).first()
            manager.first_name = request.form['first_name']
            manager.last_name = request.form['last_name']
            manager.username = request.form['username']
            manager.email = request.form['email']
            manager.phone_number = request.form['phone_number']
            manager.id_number = request.form['id_number']
            manager.save()
            flash("details updated successfully",'success')
            return redirect(url_for("manager_login"))


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
            flash("details updated successfully" ,'success')
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
            flash('The car has already been added' ,'error')
            return redirect(url_for('addcar'))
        newcar=add_car(number_plate=request.form['number_plate'],model=request.form['model'],capacity=request.form['capacity'],gear=request.form['gear'],no_of_cars=request.form['no_of_cars'],logbook_number=request.form['logbook_number'],origin=request.form['origin'],purpose=request.form['purpose'],brand=request.form['brand'],price=request.form['price'],engine=request.form['engine'],fuel=request.form['fuel'],drive_type=request.form['drive_type'],mileage=request.form['mileage'],engine_size=request.form['engine_size'],steering=request.form['steering'],min_engcc=request.form['min_engcc'],max_engcc=request.form['max_engcc'],colour=request.form['colour'],image=filename)
        newcar.save()
        flash("The car has been added successfully" ,'success') 
        return render_template("admin/add_new_car.html")             
    return render_template("admin/add_new_car.html") 

    if request.method == "GET":        
        return render_template("admin/add_new_car.html")

# @app.route("/hirecar",methods=["POST","GET"])
# def hirecar():
#     if request.method=="POST":
#         car=add_car.query.filter(add_car.number_plate==request.form['number_plate']).first()

#         customer=customer_registration.query.filter(customer_registration.username==session['user']).first()
#         if car_hire.query.filter(and_(car_hire.username==customer.username,car_hire.number_plate==customer.username)).first():
#             flash("you have already hired this car")
#             return redirect(url_for('viewcars'))
#         new_hire=car_hire(number_plate=car.number_plate,username=customer.username,phone_number=customer.phone_number,id_number=customer.id_number,email=customer.email,model=car.model,gear=car.gear,brand=car.brand,charge=((returned_date - returning_date)*1000),engine=car.engine,fuel=car.fuel,mileage=car.mileage,colour=car.colour,date_of_hire=date.now(),returning_date=date.now()+timedelta(7),hiring_id=uuid.uuid4())
#         new_hire.save()
#         flash('your hiring process has been successfully submitted kindly wait for an approval message from the manager ')
#     return redirect(url_for(''))

@app.route("/hiredcardetails", methods=["POST","GET"])
def hiredcardetails():
    if 'user' in session:
        if request.method=="POST":
            car=add_car.query.filter(add_car.number_plate==request.form['number_plate']).first()

            user=customer_registration.query.filter(customer_registration.username==session['user']).first()
            if hired_car_details.query.filter(and_(hired_car_details.username==user.username,hired_car_details.number_plate==user.username)).first():

                flash("you have already hired this car")
                return redirect(url_for('viewcarstobehired'))
            new_hire=hired_car_details(number_plate=car.number_plate,hiring_date=request.form['hiring_date'],returning_date=request.form['returning_date'],hiring_id= uuid.uuid4(),period=request.form['period'],amount=request.form['amount'],username=user.username)
            new_hire.save()
            flash('your hiring process has been successfully submitted kindly wait for an approval message from the manager','success')
            return render_template("customer/hiredcardetails.html" ,car=car)
        car=add_car.query.filter(add_car.number_plate==request.args.get('number_plate')).first()
        return render_template("customer/hiredcardetails.html",car=car)
    flash('Please login first if you have an account or create one then login','error')
    return redirect(url_for('customer_login'))
    

@app.route("/mpesas", methods=["GET","POST"])
def mpesas():
    if request.method=="POST":
        number_plate=[]
        cart=cart_table.query.filter(cart_table.username==session['user']).all()
        price =0
        # for i in cart:
        #     number_plate.append(i.number_plate)
        #     price+= int(i.price)
        # record=paymentsforcarssold(username=session['user'],number_plate=number_plate)
        # record.save()



        
        data = {
            "business_shortcode": 174379,
            "passcode": "bfb279f9aa9bdbcf158e97dd71a467cd2e0c893059b10f78e6b72ada1ed2c919",
            "amount":1,
            "phone_number": "+254758427893",
            "reference_code":"payment for car ",       
            "callback_url": "https://cab1-197-232-61-233.ap.ngrok.io/?username="+session['user'],
            "description": "Payment for a car" 
        }
        mpesa_api.MpesaExpress.stk_push(**data)
        return render_template("customer/mpesa_payment.html")

@app.route('/callback_url',methods=["POST","GET"])
def callback_url():
    json_data = request.json
    print(json_data)
    print(json_data['Body']['stkCallback']['ResultDesc'])
    if json_data['Body']['stkCallback']['ResultDesc'] == 'The service processed.' and json_data['Body']['stkCallback']['CallbackMetadata']:
        transaction_code = json_data['Body']['stkCallback']['CallbackMetadata']['Item'][1]['Value']
        amnt = json_data['Body']['stkCallback']['CallbackMetadata']['Item'][0]['value']
        phone_number = json_data['Body']['stkCallback']['CallbackMetadata']['Item'][4]['value']
        date = json_data['Body']['stkCallback']['CallbackMetadata']['Item'][3]['value']
        trans=transactions(username=request.args.get('username'),number_plate='',transaction_code=transaction_code,date=date,amnt=amnt,phone_number=phone_number)
        trans.save()

        return 'successs'

@app.route("/cart", methods=["POST","GET"])
def cart():
    if 'user' in session:

        if request.method=="GET":
            car=add_car.query.filter(add_car.number_plate==request.args.get('number_plate')).first()
            print(request.args.get('number_plate'))

            user=customer_registration.query.filter(customer_registration.username==session['user']).first()
            if cart_table.query.filter(and_(cart_table.username==user.username,cart_table.number_plate==car.number_plate)).first():

                flash("you have already added this car to the cart",'success')
                car=add_car.query.filter(add_car.purpose=='To be sold').all()
                cartitems = cart_table.query.filter(cart_table.username==session['user']).count()
                return render_template("customer/view_cars.html", car=car, cartitems=cartitems)
            cart=cart_table(number_plate=car.number_plate,cart_id= uuid.uuid4(),username=user.username,price=car.price,image=car.image)
            cart.save()
            flash('car added to the cart','success')
            return render_template("customer/view_cars2.html" ,car=car)
        car=add_car.query.filter(add_car.number_plate==request.args.get('number_plate')).first()
        return render_template("customer/view_cars2.html",car=car)
    else:
        flash('Please login first if you have an account or create one then login','error')
        return render_template("customer/customer_login.html")

@app.route("/viewcart",methods=["POST","GET"])
def viewcart():
    if request.method=="GET":
        user=customer_registration.query.filter(customer_registration.username==session['user']).first()
        cart=cart_table.query.filter(cart_table.username==session['user']).all()
        price = 0
        for i in cart:
            price+=int(i.price)

        return render_template("customer/cart.html", car=cart,price=price)



@app.route('/removefromcart',  methods=['GET', 'POST'])
def removefromcart():
    car =cart_table.query.filter(and_(cart_table.number_plate==request.args.get("number_plate")),cart_table.username==session['user']).first() 
    db.session.delete(car)
    db.session.commit()
    return redirect(url_for('viewcart'))

@app.route('/bookappointment',methods=['GET','POST'])
def bookappointment():
    if request.method=="POST":
        bkappointment=book_appointment.query.all()
        user=customer_registration.query.filter(customer_registration.username==session['user']).first()     
        bkappointment=book_appointment(appointment_id=uuid.uuid4(),number_plate=request.form['number_plate'],username=session['user'],email=request.form['email'],date=request.form['date'],location=request.form['location'],description=request.form['description'],problem=[],charges=None,appointment_state=False)
        

        adm=admin_registration.query.filter(admin_registration.role=="Repair Car").first()
        subject = "An appointment"
        body = request.form['description']
        recipients = [adm.email]
        send_mail(subject=subject,body=body,recipients=recipients)
        bkappointment.save()
        flash('your appointment has been submitted wait for feedback from the administrator via email','success')
        return render_template("customer/book_appointments.html",user=user)


    user=customer_registration.query.filter(customer_registration.username==session['user']).first()
    return render_template("customer/book_appointments.html",user=user)

@app.route("/viewappointments",methods=['POST','GET'])
def viewappointments():
    if request.method =="GET":
        if 'admin' in session:
            appointments=book_appointment.query.filter(book_appointment.appointment_state==False).all()
            return render_template("admin/view_appointments.html",appointments=appointments)
        elif 'user' in session:
            user=customer_registration.query.filter(customer_registration.username==session['user']).first()
            resp=book_appointment.query.filter(and_(book_appointment.email==user.email,book_appointment.charges!=None)).all()
            return render_template("admin/view_appointments.html",appointments=resp,user=user)

@app.route("/chargesforappointments",methods=['POST','GET'])
def chargesforappointments():
    if request.method=="POST":
        if 'admin' in session:
            charges=book_appointment.query.filter(book_appointment.appointment_id==request.form['appointment_id']).first()
            charges.problem=request.form['problem']
            charges.charges=int(request.form['charges'])

            recipients=[charges.email]
            body='The problem with your car whose number plate is:'+ charges.number_plate +'is ' +request.form['problem'] +' the charges are ksh. '+ request.form['charges']
            subject="Response for your book appointment"
            send_mail(recipients=recipients,body=body,subject=subject) 
            if charges.appointment_state==False:
                charges.appointment_state=True
            charges.save()
            return redirect(url_for('viewappointments')) 

@app.route('/declineforcarrepair',  methods=['GET', 'POST'])
def declineforcarrepair():
    car =book_appointment.query.filter(book_appointment.appointment_id==request.form['appointment_id']).first() 
    db.session.delete(car)
    db.session.commit()
    return redirect(url_for('viewappointments'))

# @app.route('/approvecarrepair',  methods=['GET', 'POST'])
# def declineforcarrepair():
#     if request.method=="POST":
#         repaircar=book_appointment.query.filter(book_appointment.appointment_id==request.form['appointment_id']).first()
#         if repaircar.approval_state==False:
#             repaircar.approval_state=True
              


@app.route('/deletecarbyadmin',  methods=['GET', 'POST'])
def deletecarbyadmin():
    if request.method=="POST":
        car =add_car.query.filter(add_car.number_plate==request.form["number_plate"]).first() 
        # if add_car.number_plate==car_hire.number_plate==number_plate==
        db.session.delete(car)
        db.session.commit()
        return redirect(url_for('viewcarsbyadmin'),car=car)
    

@app.route('/searchcars',methods=["POST","GET"])
def searchcars():
    if request.method == "POST":
        admin=admin_registration.query.filter(admin_registration.username==session['admin']).first()
        print(admin.role)
        car=add_car.query.filter(or_(add_car.number_plate==request.form['search'],add_car.brand==request.form['search'],add_car.origin==request.form['search'],add_car.fuel==request.form['search'],add_car.model==request.form['search'],add_car.gear==request.form['search'],add_car.engine==request.form['search'],add_car.steering==request.form['search'],add_car.purpose==request.form['search'])).all()
        return render_template('admin/view_cars_by_admin2.html', car=car, admin=admin)
    

@app.route('/searchcustomers',methods=["POST","GET"])
def searchcustomers():
    if request.method == "POST":
        cust=customer_registration.query.filter(or_(customer_registration.username==request.form['search'],customer_registration.first_name==request.form['search'],customer_registration.last_name==request.form['search'],customer_registration.email==request.form['search'],customer_registration.gender==request.form['search']))
        return render_template('superadmin/search_customers.html',user=cust)
        


@app.route("/about",methods=["GET","POST"])
def about():
    if request.method=="GET":
        return render_template("customer/about.html")

@app.route("/help",methods=["GET","POST"])
def help():
    if request.method=="GET":
        return render_template("customer/help.html")

@app.route('/backhome')
def backhome():
    if 'user' in session:
        return redirect(url_for("customer_login")) 
    elif 'admin' in session:
        return redirect(url_for("admin_login"))
    elif 'superadmin' in session:
        return redirect(url_for("superadmin_login"))
    elif 'manager' in session:
        return redirect(url_for("manager_login"))
    

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