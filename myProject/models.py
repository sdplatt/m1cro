from myProject import db,login_manager
from flask_login import UserMixin
from werkzeug.security import generate_password_hash,check_password_hash
import uuid

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

class User(db.Model,UserMixin):
    
    __tablename__ = 'users'

    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String)
    email = db.Column(db.String, unique=True,index=True)
    password = db.Column(db.String)
    change_pass = db.Column(db.String,unique=True)
    
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