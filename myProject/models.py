from myProject import db,login_manager
from flask_login import UserMixin
from werkzeug.security import generate_password_hash,check_password_hash
import uuid

@login_manager.user_loader
def load_user(user_id):
    return Client.query.get(user_id)

class Client(db.Model,UserMixin):
    
    __tablename__ = 'clients'

    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String)
    email = db.Column(db.String, unique=True,index=True)
    password = db.Column(db.String)
    change_pass = db.Column(db.String,unique=True)

    translations = db.relationship('Translation',backref='client',lazy=True)
    
    def __init__(self,name,email,password):
        self.name = name
        self.email = email
        self.password = generate_password_hash(password)

    def check_password(self,password):
        return check_password_hash(self.password,password)

    def changePassLink(self):
        id = str(uuid.uuid4())
        self.change_pass = id
        return id

class Translation(db.Model,UserMixin):

    __tablename__ = 'translations'
    clients = db.relationship(Client)

    id = db.Column(db.Integer,primary_key=True)
    client_id = db.Column(db.Integer,db.ForeignKey('clients.id'),nullable=False)
    language_from = db.Column(db.String)
    language_to = db.Column(db.String)
    deadline = db.Column(db.String)
    text = db.Column(db.String)
    statusId = db.Column(db.Integer,db.ForeignKey('status.id'),nullable=False)
    price = db.Column(db.Integer)
    translation = db.Column(db.String)

    def __init__(self,client_id,l_from,l_to,deadline,text,price,statusId):
        self.client_id = client_id
        self.language_from= l_from
        self.language_to = l_to
        self.deadline = deadline
        self.text = text
        self.price = price
        self.statusId = statusId

class Status(db.Model,UserMixin):

    __tablename__ = 'status'
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String,nullable=False)

    def __init__(self,name):
        self.name = name