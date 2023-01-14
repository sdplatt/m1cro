from flask import redirect,url_for,render_template,request,Blueprint,session
from myProject.models import User
from myProject.client.forms import LoginForm,RegisterationForm,ForgotPassForm,ChangePassForm
from myProject import db,mail
from flask_login import login_user, logout_user
from flask_mail import Message
from werkzeug.security import generate_password_hash

client = Blueprint('client',__name__)

@client.route('/',methods=['GET','POST'])
def home():
    # if(session['page'] == None):
    if not session.get('page'):
        session['page'] = 'login'
    # REGISTERATION FORM
    registerForm = RegisterationForm()
    if registerForm.validate_on_submit():
        user = User(name=registerForm.name.data,
                    email=registerForm.email.data,
                    password=registerForm.password.data)

        db.session.add(user)
        db.session.commit()
        return redirect(url_for('client.home'))

    # LOGIN FORM
    loginForm = LoginForm()
    if loginForm.validate_on_submit():
        user = User.query.filter_by(email=loginForm.email.data).first()

        if user is not None and user.check_password(loginForm.password.data):
            login_user(user)

            next = request.args.get('next')
            if next == None or not next[0] == '/':
                next = url_for('client.home')

            return redirect(next)
        else:
            print("Invalid login details")

    # Change Password Form
    forgotPassForm = ForgotPassForm()
    if forgotPassForm.validate_on_submit():
        user = User.query.filter_by(email=forgotPassForm.email.data).first()

        if user is not None:
            id = user.changePassLink()
            db.session.commit()
            print(id)
            msg = Message(
                'Hello',
                sender ='bansalpushkar100@gmail.com',
                recipients = [user.email]
               )
            msg.body = f'Click the link below to change your password:  {request.base_url}change/{id}'
            mail.send(msg)
            return redirect(url_for('client.home'))
    # USERS TABLE
    users = User.query.all()
    return render_template('main.html',registerForm=registerForm,loginForm=loginForm,forgotPassForm=forgotPassForm,users=users)

@client.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('client.home'))

@client.route('/forgot')
def forgot():
    session['page'] = 'forgot'
    return redirect(url_for('client.home'))

@client.route('/login')
def login():
    session['page'] = 'login'
    return redirect(url_for('client.home'))

@client.route('/register')
def register():
    session['page'] = 'register'
    return redirect(url_for('client.home'))

@client.route('/change/<id>',methods=['GET','POST'])
def change(id):
    user = User.query.filter_by(change_pass=id).first()
    if user is not None:
        changePassForm = ChangePassForm()
        if changePassForm.validate_on_submit():
            password = generate_password_hash(changePassForm.password.data)
            user.password = password
            db.session.commit()
            session['page'] = 'login'
            return redirect(url_for('client.home'))
        return render_template('change-pass.html',changePassForm=changePassForm,user=user)
    else:
        return "Page Not Found"