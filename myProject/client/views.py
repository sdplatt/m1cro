from flask import redirect,url_for,render_template,request,Blueprint,session
from myProject.models import Client,Translation,Status,Bot
from myProject.forms import LoginForm,RegisterationForm,ForgotPassForm,ChangePassForm,TranslationForm,GetPriceForm
from myProject import db,mail
from flask_login import login_user, logout_user, current_user
from flask_mail import Message
from werkzeug.security import generate_password_hash
from datetime import datetime, timedelta
import os

min_price = 0.025

client = Blueprint('client',__name__)
my_translation = None
@client.route('/',methods=['GET','POST'])
def home():
    if not session.get('page'):
        session['page'] = 'login'

    # REGISTERATION FORM
    registerForm = RegisterationForm()
    if registerForm.validate_on_submit():
        try:
            user = Client(name=registerForm.name.data,
                    email=registerForm.email.data,
                    password=registerForm.password.data)

            db.session.add(user)
            db.session.commit()
            if(session.get('email-exists')):
                session['email-exists'] = False
            session['page'] = 'login'
        except:
            session['email-exists'] = True
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
            if(session.get('invalid-login')):
                session['invalid-login'] = False
            return redirect(next)
        else:
            session['invalid-login'] = True
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
                sender ='pcktlwyr@gmail.com',
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
        if(words>350):
            session['error'] = f'Word limit is 350. You used {words} words.'
            session['curr_translation'] = {'l_from':translationForm.language_from.data,
                                            'l_to':translationForm.language_to.data,
                                            'deadline':translationForm.deadline.data,
                                            'text' : translationForm.text.data,
                                            'rejectCriteria':int(translationForm.rejectCriteria.data)}
        else:
            status = Status('new')
            db.session.add(status)
            db.session.commit()
            translation = Translation(client_id=current_user.id,
                                    l_from=translationForm.language_from.data,
                                    l_to=translationForm.language_to.data,
                                    deadline=int(translationForm.deadline.data),
                                    text = translationForm.text.data,
                                    words = words,
                                    statusId=status.id,
                                    rejectCriteria=int(translationForm.rejectCriteria.data))
            db.session.add(translation)
            db.session.commit()
            session['error'] = None
            session['popup'] = True
            session['avg_price'] = '0.08'
            my_translation = {'id': translation.id,'language_from':translation.language_from,'language_to':translation.language_to,"deadline":translation.deadline,"text":translation.text,"words":words}
            session['curr_trans'] = my_translation
        return redirect(url_for('client.home'))

    getPriceForm = GetPriceForm()
    if getPriceForm.validate_on_submit():
        price = getPriceForm.price.data
        words = my_translation['words']
        if(price/words>min_price):
            translation = Translation.query.get(my_translation['id'])
            now = datetime.utcnow()
            deadline = now + timedelta(minutes=int(my_translation['deadline'])*30)
            translation.postProcess(getPriceForm.price.data)
            translation.deadline_time = deadline
            db.session.commit()
            if(session.get('popup_close')):
                session['popup_close'] = None
            words = len(my_translation['text'].split(' '))
            msg = Message(
                'Hello',
                sender ='pcktlwyr@gmail.com',
                bcc = ['publicvince102@gmail.com','derapplikant@protonmail.com']
                )
            msg.html = f'''
            <h3>Text</h3>
            <p>{my_translation['text']}</p>
            <h3>More Details: </h3>
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
        else:
            bot = Bot.query.get(1)
            l_to = my_translation['language_to']
            api_lto = "en" if l_to=='english' else "ru" if l_to=='russian' else "de"
            obj = {'l_to':api_lto,'text':my_translation['text']}
            try:
                res = bot.translate(obj)
            except:
                res = "translated"

            translation = Translation.query.get(my_translation['id'])
            translation.botId = bot.id
            translation.postProcess(getPriceForm.price.data)
            translation.translation = res
            translation.acceptedAt=datetime.utcnow()
            translation.submittedAt=datetime.utcnow()
            db.session.commit()
            if(session.get('popup_close')):
                session['popup_close'] = None

            msg = Message(
                'Translation submitted by translator',
                sender ='pcktlwyr@gmail.com',
                recipients = [current_user.email]
                )
            msg.html = f'''
            <h3>Text</h3>
            <p>{my_translation['text']}</p>
            <h3>More Details: </h3>
            Translator's Email: {bot.email} <br>
            Translation: {my_translation['language_from']} to {my_translation['language_to']} <br>
            Price: {getPriceForm.price.data} <br>
            Total words: {words} <br>
            <br>
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
    if(session.get('error')):
        session['error'] = None
    return redirect(url_for('client.home'))

@client.route('/forgot')
def forgot():
    session['page'] = 'forgot'
    if(session.get('invalid-login')):
        session['invalid-login'] = False
    return redirect(url_for('client.home'))

@client.route('/login')
def login():
    session['page'] = 'login'
    return redirect(url_for('client.home'))

@client.route('/register')
def register():
    session['page'] = 'register'
    session['email-exists'] = False
    if(session.get('invalid-login')):
        session['invalid-login'] = False
    return redirect(url_for('client.home'))

# @client.route('/price-popup')
# def price_pop():
#     session['popup'] = True
#     return redirect(url_for('client.home'))

@client.route('/remove-popup/<id>')
def remove_price_pop(id):
    session['popup'] = False
    translation = Translation.query.get(id)
    db.session.delete(translation)
    db.session.commit()
    session['popup_close'] = True
    session['curr_translation'] = {'l_from':translation.language_from,
                                    'l_to':translation.language_to,
                                    'deadline':str(translation.deadline),
                                    'text' : translation.text,
                                    'rejectCriteria':int(translation.rejectCriteria)}
    return redirect(url_for('client.home'))

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
    if(session.get('popup_close')):
        session['popup_close'] = None
    return redirect(url_for('client.home'))

@client.route('/translation/<id>')
def show_translation(id):
    translation = Translation.query.filter_by(id=id).first()
    if(session.get('error')):
        session['error'] = None
    try:
        if(translation.translator):
            translation.email = translation.translator.email
        elif(translation.Bot):
            translation.email = translation.Bot.email
    except:
        translation.email = None
    session['trans-page'] = translation
    return redirect(url_for('client.home'))

@client.route('/rating/<id>',methods=['GET','POST'])
def submit_review(id):
    translation = Translation.query.get(id)
    rating = int(request.form.get('rating'))
    translation.rating = rating
    if(translation.translator):
        translator_rating = translation.translator.rating or 0
        rating_count = translation.translator.rating_count or 0
        translation.translator.rating_count=rating_count+1
        new_rating = (translator_rating + rating)/(rating_count+1)
        translation.translator.rating = new_rating
        msg = Message(
                    'Translation reviewd by client',
                    sender ='pcktlwyr@gmail.com',
                    recipients = [translation.translator.email]
                )
        msg.html = f'''
        <h3>Text: </h3>
        <p>{translation.text}</p>
        <h3>More Details: </h3>
        Client's Email: {translation.client.email} <br>
        Translation: {translation.language_from} to {translation.language_to} <br>
        Price: {translation.price}<br>
        Words: {translation.words}<br>
        Rating: {translation.rating}
        <br>
        '''
        mail.send(msg)
    elif (translation.Bot):
        bot_rating = translation.Bot.rating or 0
        rating_count = translation.Bot.rating_count or 0
        translation.Bot.rating_count=rating_count+1
        new_rating = (bot_rating + rating)/(rating_count+1)
        translation.Bot.rating = new_rating
    db.session.commit()
    
    return redirect(url_for('client.show_translation',id=translation.id))

@client.route('/test')
def delete_trans():
    bot = Bot.query.get(1)
    return bot.email