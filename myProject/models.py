from myProject import db,login_manager
from flask_login import UserMixin
from werkzeug.security import generate_password_hash,check_password_hash
import uuid
from datetime import datetime

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
    deadline = db.Column(db.Integer)
    text = db.Column(db.String)
    statusId = db.Column(db.Integer,db.ForeignKey('status.id'),nullable=False)
    price = db.Column(db.Integer)
    translation = db.Column(db.String)
    translatorId = db.Column(db.Integer,db.ForeignKey('translators.id'))
    rating = db.Column(db.Float())
    createdAt = db.Column(db.DateTime,default=datetime.utcnow)
    acceptedAt = db.Column(db.DateTime)
    submittedAt = db.Column(db.DateTime)

    def __init__(self,client_id,l_from,l_to,deadline,text,statusId):
        self.client_id = client_id
        self.language_from= l_from
        self.language_to = l_to
        self.deadline = deadline
        self.text = text
        self.statusId = statusId

    def postProcess(self,price):
        self.price = price

class Status(db.Model,UserMixin):

    __tablename__ = 'status'
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String,nullable=False)

    def __init__(self,name):
        self.name = name


class Service(db.Model,UserMixin): 

    __tablename__ = 'services'

    id = db.Column(db.Integer,primary_key=True)
    language_from = db.Column(db.String)
    language_to = db.Column(db.String)
    min_price = db.Column(db.Integer)
    target_price = db.Column(db.Integer)
    deadline = db.Column(db.Integer)
    translatorId = db.Column(db.Integer,db.ForeignKey('translators.id'))

    __table_args__=(db.UniqueConstraint('language_from',"language_to","translatorId",name="from_to"),)

    def __init__(self,l_from,l_to,min_price,target_price,translator,deadline):        
        self.language_from= l_from
        self.language_to = l_to
        self.min_price = min_price
        self.target_price = target_price
        self.translatorId=translator
        self.deadline = deadline

class Translator(db.Model,UserMixin):

    __tablename__ = 'translators'

    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String)
    email = db.Column(db.String, unique=True)
    password = db.Column(db.String)
    change_pass = db.Column(db.String,unique=True)
    is_human = db.Column(db.Boolean)
    translations = db.relationship('Translation',backref="translator",lazy=True)
    services = db.relationship('Service',backref="translator",lazy=True)
    rating = db.Column(db.Float(),default=0)
    rating_count = db.Column(db.Integer,default=0)

    def __init__(self,name,email,password,is_human):
        self.name = name
        self.email = email
        self.is_human = bool(is_human)
        self.password = generate_password_hash(password)

    def check_password(self,password):
        return check_password_hash(self.password,password)

    def changePassLink(self):
        id = str(uuid.uuid4())
        self.change_pass = id
        return id

    # def __repr__(self) :
    #     return f"Translator: {self.name}"