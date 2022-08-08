from enum import unique
from operator import add
import re
from flask_sqlalchemy import SQLAlchemy 
from passlib.hash import sha256_crypt
db=SQLAlchemy()

class customer_registration(db.Model):
        __tablename__='customer_registration'
        first_name=db.Column(db.String,nullable=False)
        last_name=db.Column(db.String,nullable=False)
        username=db.Column(db.String,primary_key=True, nullable=False)
        id_number=db.Column(db.String,nullable=False,unique=True)
        phone_number=db.Column(db.Integer,nullable=False, unique=True)
        email=db.Column(db.String,nullable=False)
        gender=db.Column(db.String,nullable=False)
        password=db.Column(db.String ,nullable=False)
        def __init__(self,first_name,last_name,username, id_number, phone_number,email,gender,password):
                self.first_name=first_name
                self.last_name=last_name
                self.username=username
                self.id_number=id_number
                self.phone_number=phone_number
                self.email=email
                self.gender=gender
                self.password=sha256_crypt.encrypt(password)

        def save(self):
                db.session.add(self)
                db.session.commit() 

class staff_registration(db.Model):
        __tablename__='staff_registration'
        first_name=db.Column(db.String,nullable=False)
        last_name=db.Column(db.String,nullable=False)
        username=db.Column(db.String,primary_key=True, nullable=False)
        id_number=db.Column(db.String,nullable=False,unique=True)
        phone_number=db.Column(db.Integer,nullable=False, unique=True)
        role=db.Column(db.String,nullable=False)
        email=db.Column(db.String,nullable=False)
        gender=db.Column(db.String,nullable=False)
        password=db.Column(db.String ,nullable=False)
        def __init__(self,first_name,last_name,username, id_number, phone_number,role,email,gender,password):
                self.first_name=first_name
                self.last_name=last_name
                self.username=username
                self.id_number=id_number
                self.phone_number=phone_number
                self.role=role
                self.email=email
                self.gender=gender
                self.password=sha256_crypt.encrypt(password)

        def save(self):
                db.session.add(self)
                db.session.commit()

class admin_registration(db.Model):
        __tablename__='admin_registration'
        first_name=db.Column(db.String,nullable=False)
        last_name=db.Column(db.String,nullable=False)
        username=db.Column(db.String,primary_key=True, nullable=False)
        id_number=db.Column(db.Integer,nullable=False,unique=True)
        phone_number=db.Column(db.Integer,nullable=False, unique=True)
        email=db.Column(db.String,nullable=False)
        gender=db.Column(db.String,nullable=False)
        role=db.Column(db.String,nullable=False)
        password=db.Column(db.String ,nullable=False)
        def __init__(self,first_name,last_name,username, id_number, phone_number,email,role,gender,password):
                self.first_name=first_name
                self.last_name=last_name
                self.username=username
                self.id_number=id_number
                self.phone_number=phone_number
                self.email=email
                self.role=role
                self.gender=gender
                self.password=sha256_crypt.encrypt(password)

        def save(self):
                db.session.add(self)
                db.session.commit()
        def serialize(self):
                return {
                        'first_name':self.first_name,
                        'last_name':self.last_name,
                        'username':self.username,
                        'email':self.email,
                        'id_number':self.id_number,
                        'phone_number':self.phone_number,
                        'gender':self.gender,
                        'role':self.role,
                }

class manager_registration(db.Model):
        __tablename__='manager_registration'
        first_name=db.Column(db.String,nullable=False)
        last_name=db.Column(db.String,nullable=False)
        username=db.Column(db.String,unique=True, nullable=False,primary_key=True)
        staff_id=db.Column(db.String,unique=True, nullable=False)
        id_number=db.Column(db.Integer,nullable=False,unique=True)
        phone_number=db.Column(db.Integer,nullable=False, unique=True)
        email=db.Column(db.String,nullable=False)
        gender=db.Column(db.String,nullable=False)
        role=db.Column(db.String,nullable=False)
        password=db.Column(db.String ,nullable=False)
        def __init__(self,first_name,last_name,username,staff_id, id_number, phone_number,email,role,gender,password):
                self.first_name=first_name
                self.last_name=last_name
                self.username=username
                self.staff_id=staff_id
                self.id_number=id_number
                self.phone_number=phone_number
                self.email=email
                self.role=role
                self.gender=gender
                self.password=sha256_crypt.encrypt(password)

        def save(self):
                db.session.add(self)
                db.session.commit()


class superadmin_registration(db.Model):
        __tablename__='superadmin_registration'
        first_name=db.Column(db.String,nullable=False)
        last_name=db.Column(db.String,nullable=False)
        username=db.Column(db.String,primary_key=True, nullable=False)
        id_number=db.Column(db.Integer,nullable=False,unique=True)
        phone_number=db.Column(db.Integer,nullable=False, unique=True)
        email=db.Column(db.String,nullable=False)
        gender=db.Column(db.String,nullable=False)
        role=db.Column(db.String,nullable=False)
        password=db.Column(db.String ,nullable=False)
        def __init__(self,first_name,last_name,username, id_number, phone_number,email,gender,role,password):
                self.first_name=first_name
                self.last_name=last_name
                self.username=username
                self.id_number=id_number
                self.phone_number=phone_number
                self.email=email
                self.gender=gender
                self.role=role                
                self.password=sha256_crypt.encrypt(password)

        def save(self):
                db.session.add(self)
                db.session.commit()


class add_car(db.Model):
        __tablename__='add_car'
        number_plate=db.Column(db.String,nullable=False, primary_key=True)
        model=db.Column(db.String,nullable=False)
        capacity=db.Column(db.Integer, nullable=False)
        gear=db.Column(db.String,nullable=False)
        no_of_cars=db.Column(db.Integer,nullable=False)
        logbook_number=db.Column(db.String,nullable=False,unique=True)
        origin=db.Column(db.String,nullable=False)
        brand=db.Column(db.String,nullable=False)
        price=db.Column(db.Integer)
        engine=db.Column(db.String,nullable=False)
        purpose=db.Column(db.String,nullable=True)

        fuel=db.Column(db.String,nullable=False)
        drive_type=db.Column(db.String,nullable=False)
        mileage=db.Column(db.String,nullable=False)
        engine_size=db.Column(db.String,nullable=False)
        steering=db.Column(db.String,nullable=False)
        min_engcc=db.Column(db.String,nullable=False)
        max_engcc=db.Column(db.String,nullable=False)
        colour=db.Column(db.String,nullable=False)
        
        image=db.Column(db.String,nullable=False)

        def __init__(self,number_plate,model,capacity,gear,no_of_cars,logbook_number,origin,brand,price,engine,fuel,drive_type,mileage,engine_size,steering,purpose,min_engcc,max_engcc,colour,image):
                self.number_plate=number_plate
                self.model=model
                self.capacity=capacity
                self.gear=gear
                self.no_of_cars=no_of_cars
                self.logbook_number=logbook_number
                self.origin=origin
                self.brand=brand  
                self.price=price 
                self.engine=engine
                self.purpose=purpose

                self.fuel=fuel
                self.drive_type=drive_type
                self.mileage=mileage
                self.engine_size=engine_size
                self.steering=steering
                self.min_engcc=min_engcc
                self.max_engcc=max_engcc
                self.colour=colour


                self.image=image          

        def save(self):
                db.session.add(self)
                db.session.commit()

# class car_hire(db.Model):
#         __tablename__='car_hire'
#         hiring_id=db.Column(db.String,nullable=False,primary_key=True)
#         username = db.Column(db.String ,db.ForeignKey('customer_registration.username'),nullable=False)
#         id_number=db.Column(db.Integer,nullable=False,unique=True)
#         phone_number=db.Column(db.Integer,nullable=False, unique=True)
#         email=db.Column(db.String,nullable=False)
#         number_plate = db.Column(db.String ,db.ForeignKey('customer_registration.number_plate'),nullable=False)
#         model=db.Column(db.String,nullable=False)
#         gear=db.Column(db.String,nullable=False)
#         brand=db.Column(db.String,nullable=False)
#         charges=db.Column(db.Integer,nullable=False)
#         engine=db.Column(db.String,nullable=False)
#         fuel=db.Column(db.String,nullable=False)
#         mileage=db.Column(db.String,nullable=False)
#         colour=db.Column(db.String,nullable=False)
#         date_of_hire=db.Column(db.String,nullable=False)
#         returning_date=db.Column(db.String,nullable=False)

#         def __init__(self,hiring_id,username, id_number,phone_number,email,number_plate,model,gear,brand,charges,engine,fuel,mileage,colour,date_of_hire,returning_date):
#                 self.hiring_id=hiring_id
#                 self.username=username
#                 self.id_number=id_number
#                 self.phone_number=phone_number
#                 self.email=email
#                 self.number_plate=number_plate
#                 self.model=model    
#                 self.gear=gear 
#                 self.brand=brand
#                 self.charges=charges
#                 self.engine=engine
#                 self.fuel=fuel
#                 self.mileage=mileage
#                 self.colour=colour
#                 self.date_of_hire=date_of_hire
#                 self.returning_date=returning_date 

        # def save(self):
        #         db.session.add(self)
        #         db.session.commit()

class hired_car_details(db.Model):
        __tablename__='hired_car_details'
        number_plate=db.Column(db.String,db.ForeignKey('add_car.number_plate'),nullable=False, unique=True)
        username=db.Column(db.String,db.ForeignKey('customer_registration.username'),nullable=False)
        hiring_id=db.Column(db.String,primary_key=True)
        hiring_date=db.Column(db.String,nullable=False)
        returning_date=db.Column(db.String,nullable=False)
        period=db.Column(db.String, nullable=False)
        amount=db.Column(db.Integer,nullable=False)
        
        def __init__(self,number_plate,hiring_id,hiring_date,returning_date,period,amount,username):
                self.number_plate=number_plate
                self.hiring_id=hiring_id
                self.hiring_date=hiring_date
                self.returning_date=returning_date
                self.period=period
                self.username=username
                self.amount=amount

        def save(self):
                db.session.add(self)
                db.session.commit()


class cart_table(db.Model):
        __tablename__='cart_table'
        number_plate=db.Column(db.String,db.ForeignKey('add_car.number_plate'),nullable=False, unique=True)
        username=db.Column(db.String,db.ForeignKey('customer_registration.username'),nullable=False)
        price=db.Column(db.String,nullable=False)
        image=db.Column(db.String,nullable=False)
        cart_id=db.Column(db.String,primary_key=True)
                
        def __init__(self,number_plate,cart_id,username,price,image):
                self.number_plate=number_plate
                self.cart_id=cart_id
                self.username=username
                self.price=price
                self.image=image
        def save(self):
                db.session.add(self)
                db.session.commit()

class transactions(db.Model):
        __tablename__='transactions'
        number_plate=db.Column(db.String,nullable=False, unique=True)
        username=db.Column(db.String,nullable=False,unique=True)
        transaction_code=db.Column(db.String,unique=True,primary_key=True)
        amnt=db.Column(db.String,nullable=False)
        date=db.Column(db.String,nullable=False)
        phone_number=db.Column(db.String,nullable=False,unique=True)
                
        def __init__(self,number_plate,username,transaction_code,amnt,date,phone_number):
                self.number_plate=number_plate
                self.username=username
                self.transaction_code=transaction_code
                self.amnt=amnt
                self.date=date
                self.phone_number=phone_number
        def save(self):
                db.session.add(self)
                db.session.commit()

class paymentsforcarssold(db.Model):
        __tablename__='paymentsforcarssold'
        number_plate=db.Column(db.ARRAY(db.String),nullable=False, unique=True)
        username=db.Column(db.String,nullable=False,unique=True,primary_key=True)           
        def __init__(self,number_plate,username):
                self.number_plate=number_plate
                self.username=username
        def save(self):
                db.session.add(self)
                db.session.commit()

class book_appointment(db.Model):
        __tablename__='book_appointment'

        appointment_id=db.Column(db.String,nullable=False, unique=True,primary_key=True)
        number_plate=db.Column(db.String,nullable=False)
        username=db.Column(db.String,db.ForeignKey('customer_registration.username'),nullable=False)
        email=db.Column(db.String,nullable=False)
        date=db.Column(db.String,nullable=False)
        location=db.Column(db.String,nullable=False)
        description=db.Column(db.String,nullable=False)
        problem=db.Column(db.String)
        charges=db.Column(db.Integer)
        appointment_state=db.Column(db.Boolean)
                
        def __init__(self,appointment_id,number_plate,username,email,date,location,description,problem,charges,appointment_state):
                self.appointment_id=appointment_id
                self.number_plate=number_plate
                self.username=username
                self.email=email
                self.date=date
                self.location=location
                self.description=description
                self.problem=problem
                self.charges=charges
                self.appointment_state=appointment_state
        def save(self):
                db.session.add(self)
                db.session.commit()


# class buy_transaction(db.Model):
#         __tablename__='buy_transaction'
#         number_plate=db.Column(db.String,db.ForeignKey('add_car.number_plate'),nullable=False, unique=True)
#         username=db.Column(db.String,db.ForeignKey('customer_registration.username'),nullable=False)
#         transaction_code=db.Column(db.String,unique=True)
#         buy_id=db.Column(db.String,primary_key=True)
                
#         def __init__(self,number_plate,username,transaction_code,buy_id):
#                 self.number_plate=number_plate
#                 self.username=username
#                 self.transaction_code=transaction_code
#                 self.buy_id=buy_id
#         def save(self):
#                 db.session.add(self)
#                 db.session.commit()


# class hire_transaction(db.Model):
#         __tablename__='hire_transaction'
#         number_plate=db.Column(db.String,db.ForeignKey('add_car.number_plate'),nullable=False, unique=True)
#         username=db.Column(db.String,db.ForeignKey('customer_registration.username'),nullable=False)
#         transaction_code=db.Column(db.String,unique=True)
#         hire_id=db.Column(db.String,primary_key=True)
                
#         def __init__(self,number_plate,username,transaction_code,hire_id):
#                 self.number_plate=number_plate
#                 self.username=username
#                 self.transaction_code=transaction_code
#                 self.hire_id=hire_id
#         def save(self):
#                 db.session.add(self)
#                 db.session.commit()