from flask import redirect,url_for,render_template,request,Blueprint,session
from myProject.models import Client,Translation,Status
from myProject.forms import LoginForm,RegisterationForm,ForgotPassForm,ChangePassForm,TranslationForm,GetPriceForm
from myProject import db,mail
from flask_login import login_user, logout_user, current_user
from flask_mail import Message
from werkzeug.security import generate_password_hash
from datetime import datetime, timedelta

client = Blueprint('client',__name__)
my_translation = None
@client.route('/',methods=['GET','POST'])
def home():
    if not session.get('page'):
        session['page'] = 'login'

    # REGISTERATION FORM
    registerForm = RegisterationForm()
    if registerForm.validate_on_submit():
        user = Client(name=registerForm.name.data,
                    email=registerForm.email.data,
                    password=registerForm.password.data)

        db.session.add(user)
        db.session.commit()
        session['page'] = 'login'
        return redirect(url_for('client.home'))

    # LOGIN FORM
    loginForm = LoginForm()
    if loginForm.validate_on_submit():
        user = Client.query.filter_by(email=loginForm.email.data).first()

        if user is not None and user.check_password(loginForm.password.data):
            login_user(user)

            next = request.args.get('next')
            if next == None or not next[0] == '/':
                next = url_for('client.home')

            session['trans-page'] = 'create'
            session['user'] = 'client'
            return redirect(next)
        else:
            print("Invalid login details")
            return redirect(url_for('client.home'))

    # Change Password Form
    forgotPassForm = ForgotPassForm()
    if forgotPassForm.validate_on_submit():
        user = Client.query.filter_by(email=forgotPassForm.email.data).first()

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
    users = Client.query.all()

    # translations form
    translationForm = TranslationForm()
    
    if translationForm.validate_on_submit():
        global my_translation
        text = translationForm.text.data
        words = len(text.split(' '))
        if(words>300):
            session['error'] = f'Word limit is 300. You used {words} words.'
        else:
            status = Status('new')
            db.session.add(status)
            db.session.commit()
            translation = Translation(client_id=current_user.id,
                                    l_from=translationForm.language_from.data,
                                    l_to=translationForm.language_to.data,
                                    deadline=translationForm.deadline.data,
                                    text = translationForm.text.data,
                                    statusId=status.id)
            db.session.add(translation)
            db.session.commit()
            session['error'] = None
            session['popup'] = True
            my_translation = {'id': translation.id,'language_from':translation.language_from,'language_to':translation.language_to,"deadline":translation.deadline,"text":translation.text}
        return redirect(url_for('client.home'))

    getPriceForm = GetPriceForm()
    if getPriceForm.validate_on_submit():
        translation = Translation.query.get(my_translation['id'])
        translation.postProcess(getPriceForm.price.data)
        db.session.commit()
        now = datetime.utcnow()
        deadline = now + timedelta(minutes=int(my_translation['deadline'])*30)
        words = len(my_translation['text'].split(' '))
        msg = Message(
            'Hello',
            sender ='bansalpushkar100@gmail.com',
            recipients = ['bansalpushkar99@gmail.com',"random@gmail.com"]
            )
        msg.html = f'''
        Client's Email: {current_user.email} <br>
        Translation: {my_translation['language_from']} to {my_translation['language_to']} <br>
        Price: {getPriceForm.price.data} <br>
        Total words: {words} <br>
        Deadline: {deadline} <br>
        <br>
        <p>
        Click <a href="{request.base_url}translator/accept-page/{my_translation['id']}">here</a> to accept or reject the translation.
        </p>
        '''
        mail.send(msg)
        session['popup'] = False
        my_translation = None
        return redirect(url_for('client.home'))
    
    # TRANSLATIONS TABLE
    try:
        translations = Client.query.filter_by(id=current_user.id).first().translations
    except:
        translations = []
    return render_template('client.html',registerForm=registerForm,loginForm=loginForm,forgotPassForm=forgotPassForm,users=users,translationForm=translationForm,translations=translations,getPriceForm=getPriceForm,translation=my_translation)

@client.route('/logout')
def logout():
    logout_user()
    session['user'] = None
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

# @client.route('/price-popup')
# def price_pop():
#     session['popup'] = True
#     return redirect(url_for('client.home'))

# @client.route('/remove-popup')
# def remove_price_pop():
#     session['popup'] = False
#     session['translator'] = None
#     return redirect(url_for('client.home'))

@client.route('/change/<id>',methods=['GET','POST'])
def change(id):
    user = Client.query.filter_by(change_pass=id).first()
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

# TRANSLATIONS
@client.route('/create-translation')
def create_translation():
    session['trans-page'] = "create"
    return redirect(url_for('client.home'))

@client.route('/translation/<id>')
def show_translation(id):
    translation = Translation.query.filter_by(id=id).first()
    session['trans-page'] = translation
    return redirect(url_for('client.home'))

# @client.route('/test')
# def delete_trans():
    # translations = Service.query.delete()
    # db.session.commit()
