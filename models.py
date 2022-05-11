from enum import unique
from operator import add
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
        image=db.Column(db.String,nullable=False)

        def __init__(self,number_plate,model,capacity,gear,no_of_cars,logbook_number,origin,brand,price,engine,image):
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
                self.image=image          

        def save(self):
                db.session.add(self)
                db.session.commit()