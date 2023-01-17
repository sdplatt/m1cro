from flask import redirect,url_for,render_template,request,Blueprint,session
from myProject.models import Translation,Translator,Service
from myProject.forms import LoginForm,ForgotPassForm,ChangePassForm,RegisterTranslator,AddServiceForm
from myProject import db,mail
from flask_login import login_user, logout_user, current_user
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
                    is_human=True)

        db.session.add(user)
        db.session.commit()
        session['page'] = 'login'
        return redirect(url_for('translator.home'))

    # LOGIN FORM
    loginForm = LoginForm()
    if loginForm.validate_on_submit():
        global myUser
        user = Translator.query.filter_by(email=loginForm.email.data).first()

        if user is not None and user.check_password(loginForm.password.data):
            login_user(user)
            myUser = user
            session['id'] = current_user.id
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
            msg.body = f'Click the link below to change your password:  {request.base_url}/change/{id}'
            mail.send(msg)
            return redirect(url_for('translator.home'))

    # ADD SERVICE FORM
    addServiceForm = AddServiceForm()
    if addServiceForm.validate_on_submit():
        # try:
            service = Service(l_from=addServiceForm.language_from.data,
                        l_to=addServiceForm.language_to.data,
                        min_price=addServiceForm.min_price.data,
                        target_price=addServiceForm.target_price.data,
                        translator=session.get('id'))
            db.session.add(service)
            db.session.commit()
        # except:
        #     return redirect(url_for('translator.home'))
    # USERS TABLE
    users = Translator.query.all()

    # SERVICES
    try:
        services = Translator.query.filter_by(id=session.get('id')).first().services
    except:
        services = []
    
    return render_template('translator.html',registerForm=registerForm,loginForm=loginForm,forgotPassForm=forgotPassForm,users=users,user=myUser,services=services,addServiceForm=addServiceForm)

@translator.route('/logout')
def logout():
    session['user'] = None
    logout_user()
    session[id] = None
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


@translator.route('/change/<id>',methods=['GET','POST'])
def change(id):
    user = Translator.query.filter_by(change_pass=id).first()
    if user is not None:
        changePassForm = ChangePassForm()
        if changePassForm.validate_on_submit():
            password = generate_password_hash(changePassForm.password.data)
            user.password = password
            db.session.commit()
            session['page'] = 'login'
            return redirect(url_for('translator.home'))
        return render_template('change-pass.html',changePassForm=changePassForm,user=user)
    else:
        return "Page Not Found"