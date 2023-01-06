
from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy
from app import db
from datetime import datetime
from werkzeug.security import generate_password_hash,check_password_hash



class Users(db.Model,UserMixin):
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(200),nullable=False)
    email = db.Column(db.String(120),nullable=False, unique=True)
    date_added = db.Column(db.DateTime, default=datetime.utcnow)
    # password work stuff
    password_hash = db.Column(db.String(128))
    orders = db.relationship('Sales', backref='sales') #name to use for referencing

    @property
    def password(self):
        raise AttributeError('Password does not have a read attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash

    def verify_password(self,password):
        return check_password_hash(self.password_hash, password)


    # Create a string
    def __repr__(self):
        return '<Name %r>' % self.name 

#Instance a new database table "once" from python interpreter 
#Type "python" in terminal
#>> from app import db,app
#>> db.init_app(app=app)
#>> with app.app_context():
#....   db.create_all()  
#>> exit()

# Creating an Items table

class Sales(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    size = db.Column(db.String())
    quantity = db.Column(db.Integer())
    order_date = db.Column(db.DateTime, default=datetime.utcnow)
    orderer_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    

class Items(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    size = db.Column(db.String(255))
    price = db.Column(db.Integer())

