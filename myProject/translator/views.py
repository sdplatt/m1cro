from flask import redirect,url_for,render_template,request,Blueprint,session
from myProject.models import Client,Translation,Status,Translator
from myProject.forms import LoginForm,RegisterTranslator,ForgotPassForm,ChangePassForm,TranslationForm
from myProject import db,mail
# from flask_login import login_user, logout_user, current_user
from flask_mail import Message
from werkzeug.security import generate_password_hash

translator = Blueprint('translator',__name__,url_prefix='/translator')
myUser = None
@translator.route('/',methods=['GET','POST'])
def home():
    if not session.get('page'):
        session['page'] = 'login'

    # REGISTERATION FORM
    registerForm = RegisterTranslator()
    if registerForm.validate_on_submit():
        user = Translator(name=registerForm.name.data,
                    email=registerForm.email.data,
                    password=registerForm.password.data,
                    l_from=registerForm.language_from.data,
                    l_to=registerForm.language_to.data,
                    min_price=registerForm.min_price.data,
                    target_price=registerForm.target_price.data)

        db.session.add(user)
        db.session.commit()
        session['page'] = 'login'
        return redirect(url_for('translator.home'))

    # LOGIN FORM
    loginForm = LoginForm()
    if loginForm.validate_on_submit():
        global myUser
        user = Translator.query.filter_by(email=loginForm.email.data).first()
        myUser = user
        if user is not None and user.check_password(loginForm.password.data):

            next = request.args.get('next')
            if next == None or not next[0] == '/':
                next = url_for('translator.home')

            session['user'] = 'translator'
            
            return redirect(next)
        else:
            print("Invalid login details")
            return redirect(url_for('translator.home'))

    # Change Password Form
    forgotPassForm = ForgotPassForm()
    if forgotPassForm.validate_on_submit():
        user = Translator.query.filter_by(email=forgotPassForm.email.data).first()

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
            return redirect(url_for('translator.home'))
    # USERS TABLE
    users = Translator.query.all()
    
    
    return render_template('translator.html',registerForm=registerForm,loginForm=loginForm,forgotPassForm=forgotPassForm,users=users,user=myUser)

@translator.route('/logout')
def logout():
    session['user'] = None
    return redirect(url_for('translator.home'))

@translator.route('/forgot')
def forgot():
    session['page'] = 'forgot'
    return redirect(url_for('translator.home'))

@translator.route('/login')
def login():
    session['page'] = 'login'
    return redirect(url_for('translator.home'))

@translator.route('/register')
def register():
    session['page'] = 'register'
    return redirect(url_for('translator.home'))