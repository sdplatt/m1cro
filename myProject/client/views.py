from flask_babel import gettext
from flask import redirect,url_for,render_template,request,Blueprint,session,current_app
from myProject.models import Client, GlossaryPair,Translation,Status,Bot
from myProject.forms import LoginForm,RegisterationForm,ForgotPassForm,ChangePassForm,TranslationForm,GetPriceForm, GlossaryPairForm
from myProject import db,mail
from flask_login import login_user, logout_user, current_user
from flask_mail import Message
from werkzeug.security import generate_password_hash
from datetime import datetime, timedelta
from pytz import timezone
from jinja2 import Template

client = Blueprint('client',__name__)
my_translation = None
@client.route('/',methods=['GET','POST'])
def home():
    if not session.get('page'):
        session['page'] = 'login'
    #CONFIG VARS
    max_default_word_len = current_app.config["MAX_WORD_LENGTH"]
    min_word_price = current_app.config["MIN_WORD_PRICE"]
    site_time_zone = current_app.config["SITE_TIMEZONE"]
    site_title = current_app.config["SITE_TITLE"]
    site_admin = current_app.config["SITE_ADMIN"]
    site_currency = current_app.config["SITE_CURRENCY"]
    grace_period = 10
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
            basicGreeting = gettext("Hello from")
            subject = "{} {}".format(basicGreeting, site_title)
            sender = "{}".format(site_admin) 
            msg = Message(
                subject,
                sender =sender,
                recipients = [user.email]
            )
            changePasswordPrompt = gettext('Click the link below to change your password')
            msg.body = f"{changePasswordPrompt}: {request.base_url}change/{id}"
            mail.send(msg)
            return redirect(url_for('client.home'))
    # USERS TABLE
    users = Client.query.all()

    # translations form
    translationForm = TranslationForm()
    if not session.get('glossary-pairs'):
        session['glossary-pairs'] = 6
    """
    GLoassry Pair form is the add_glossary_pair i the Translation form which serves as the DyanmicForm
    is used to dynamically add more instances of the glossaryPair in the Translatin create frm
    """
    if translationForm.validate_on_submit():

        global my_translation
        text = translationForm.text.data
        words = len(text.split(' '))
        translationForm.deadline.data =  30
        translationForm.rejectCriteria.data = 1
        
        if(words>max_default_word_len):
            session['error'] = f"{gettext('Word limit is')} {max_default_word_len}. {gettext('You have {words} words.')}"
            session['curr_translation'] = {'l_from':translationForm.language_from.data,
                                            'l_to':translationForm.language_to.data,
                                            'deadline':translationForm.deadline.data,
                                            'text' : translationForm.text.data,
                                            'rejectCriteria':int(translationForm.rejectCriteria.data)}
        else:
            #ELSE: Source is suffic. small good to go
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
                                    rejectCriteria=int(translationForm.rejectCriteria.data)
                                    )
            db.session.add(translation)
            db.session.commit()
            for i in range(1,session.get('glossary-pairs')+1):
                pair = GlossaryPair(sourceText=translationForm['glossary_pair_{}'.format(i)].sourceText.data,
                                    targetText=translationForm['glossary_pair_{}'.format(i)].targetText.data,
                                    translationId=translation.id)
                db.session.add(pair)
                db.session.commit()
            session['error'] = None
            session['popup'] = True
            session['avg_price'] = "{:.2f}".format(0.08*words) #this will come from DB
            session['min_price'] = "{:.2f}".format(min_word_price*words)
            now = datetime.now(timezone(site_time_zone))
            #BUG this is incorrect!!!!!
            session['deadline_as_time'] = (datetime.now(timezone(site_time_zone)) + timedelta(minutes=int(grace_period) + int(translationForm.deadline.data)*30)).strftime("%H:%M")
            glosaaryPairs = [f"{i.sourceText} -> {i.targetText}" for i in translation.glosssaryPairs]
            my_translation = {'id': translation.id,'language_from':translation.language_from,'language_to':translation.language_to,"deadline":translation.deadline,"text":translation.text,"words":words,"glossaryPairs":glosaaryPairs}
            session['curr_trans'] = my_translation
        return redirect(url_for('client.home'))

    getPriceForm = GetPriceForm()
    if getPriceForm.validate_on_submit():
        session['glossary-pairs'] = 6
        price = getPriceForm.price.data
        words = my_translation['words']
        if(price/words>=min_word_price):
            """if at or above threshold call humans"""
            translation = Translation.query.get(my_translation['id'])
            now = datetime.now(timezone(site_time_zone))
            #this information needs to be hidden!
            beta_testers = ['exitnumber3@mail.ru']
            candidates = ['publicvince102@gmail.com','deruen@proton.me', 'exitnumber3@mail.ru', 'publicvince103@gmail.com',"bansalpushkar100@gmail.com"]
            #new_candidates = list(set(beta_testers + candidates)) #use later
            if current_user.email in candidates:
                candidates.remove(current_user.email)
            deadline = datetime.now(timezone(site_time_zone)) + timedelta(minutes=int(grace_period) + int(my_translation['deadline'])*30)
            translation.postProcess(getPriceForm.price.data)
            translation.deadline_time = deadline.astimezone(timezone(site_time_zone)) #Now ALL CET!!!
            db.session.commit()
            if(session.get('popup_close')):
                session['popup_close'] = None
            words = len(my_translation['text'].split(' '))
            msg = Message(
                '''A Job offer from {site_title}''',
                sender ='pcktlwyr@gmail.com',
                bcc = candidates
                )
            msg.html = f'''
            <h3>Text</h3>
            <p>{my_translation['text']}</p>
            <h3>More Details: </h3>
            Client's email: {current_user.email} <br>
            Translation: {my_translation['language_from']} to {my_translation['language_to']} <br>
            Price: {site_currency} {getPriceForm.price.data} <br>
            Total words: {words} <br>
            Current_time: {now.strftime("%H:%M")} CET <br>
            Deadline: {deadline.strftime("%H:%M")} CET <br>
            <h4>Glossary Pairs</h4>
            {','.join(my_translation['glossaryPairs'])}
            <br>
            <p>
            Click <a href="{request.base_url}translator/accept-page/{my_translation['id']}">here</a> to accept or reject the translation.
            Please deliver on time. You will not get another chance! Scroll down for other languages
            </p>
            '''
            mail.send(msg)
        else:
            """Call bot; Prepare DB first"""
            bot = Bot.query.get(1) #1 DB
            l_to = my_translation['language_to']
            api_lto = "en" if l_to=='english' else "ru" if l_to=='russian' else "de"
            obj = {'l_to':api_lto,'text':my_translation['text']}
            try:
                #delay here using asyncio, threading, or multiprocessing libraries. non blocking!
                res = bot.translate(obj)
            except:
                #indicates a problem with the API call try to regenerate 12 hour key here
                #call getNewKey() or have a worker do it every 24 hours export IAMTOKEN=$(yc iam create-token) export FOLDERID
                res = '''Please contact the help desk on {site_admin}'''

            translation = Translation.query.get(my_translation['id'])
            translation.botId = bot.id
            translation.postProcess(getPriceForm.price.data)
            translation.translation = res
            translation.acceptedAt=datetime.now(timezone(site_time_zone))
            translation.submittedAt=datetime.now(timezone(site_time_zone))
            db.session.commit()
            if(session.get('popup_close')):
                session['popup_close'] = None

            msg = Message(
                'A translation has been submitted by a Translator',
                sender ='pcktlwyr@gmail.com',
                recipients = [current_user.email]
                )
            msg.html = f'''
            <div style="color:black">
            <h3>Source text</h3>
            <p>{my_translation['text']}</p>
            <h3>More details: </h3>
            Translator's email: {bot.email} <br>
            Translation: {my_translation['language_from']} to {my_translation['language_to']} <br>
            Price: {getPriceForm.price.data} <br>
            Total words: {words} <br>
            <h4>Glossary Pairs</h4>
            {','.join(my_translation['glossaryPairs'])}
            <br>
            Click HERE to view and review the translation.
            </div>
            '''
            mail.send(msg)

        session['popup'] = False
        # my_translation = None
        return redirect(url_for('client.show_translation',id=my_translation['id']))
    
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
    curr_translation = {'l_from':translation.language_from,
                                    'l_to':translation.language_to,
                                    'deadline':str(translation.deadline),
                                    'text' : translation.text,
                                    'rejectCriteria':int(translation.rejectCriteria)}
    for i,pair in enumerate(translation.glosssaryPairs):
        curr_translation[f"glossary_pair_{i}"] = {'source':pair.sourceText,"target":pair.targetText}
    session['curr_translation'] = curr_translation

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
    session['glossary-pairs'] = 6
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
                    'A Translation has been reviewed and accepted by a Client',
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
    translation = Translation.query.get(7)
    translation.translation = 'Lorem ipsum dolor sit, amet consectetur adipisicing elit. Dicta explicabo, quae facilis fugit deserunt error? Temporibus nobis veniam sed repellat at deleniti, alias laboriosam, vel, aspernatur laborum est! Eum, magnam repellat! Sunt alias repellat culpa ratione quod maxime, enim blanditiis expedita sequi sint quae tempora modi dolorem iste, mollitia debitis reiciendis? Quos illum eum mollitia odio libero ipsum? Rerum eaque quam corrupti inventore ipsa maxime modi voluptatibus doloribus eos error aspernatur neque commodi consectetur quae, vitae illum at a placeat voluptatem magni? Commodi, necessitatibus corrupti laboriosam ipsa sint quis perferendis aut dolorum non, nam soluta blanditiis natus. Dolorum fuga modi aut quisquam, possimus omnis eius excepturi aliquid et, enim vero architecto ipsum ipsam minima delectus ea iste sapiente voluptas veritatis recusandae unde commodi culpa iure. Quas, sit nesciunt mollitia expedita doloribus neque optio asperiores nulla iusto fuga commodi veritatis vel quae eos labore hic rem aperiam totam soluta? Aut voluptatibus nisi commodi officia itaque nihil nobis esse velit voluptates optio tempora vitae laboriosam sed magni obcaecati, quasi unde impedit reiciendis inventore, ratione porro consequuntur illum fuga cumque? Quam, possimus! Facere laboriosam esse odit quae quia dolore rerum sint aliquam pariatur quasi temporibus harum eveniet debitis praesentium quas enim eaque, autem, nostrum illo. Dolorum eaque dolore quam possimus eum quas minus reiciendis, nam pariatur beatae molestiae voluptatem quo nobis, hic explicabo unde, odio provident assumenda placeat? Sequi error dicta molestias debitis alias minus necessitatibus reprehenderit reiciendis temporibus nam molestiae porro, quas distinctio? Tempora excepturi provident nihil iusto fugiat dolores ducimus necessitatibus neque ipsum. Eligendi, quae? Quod dignissimos totam voluptate, aliquid molestiae modi iusto facere nulla nesciunt, at expedita nihil, in molestias officiis aliquam? Accusamus fugit reprehenderit, similique harum maxime repudiandae. Tempora repudiandae culpa libero consequatur, quos natus rerum. Quas laborum nihil magni vero porro natus dolorum magnam consequatur incidunt saepe distinctio recusandae quo fugiat esse sit harum tenetur, maiores eum aut autem! Non mollitia asperiores optio consequatur quidem molestiae, fuga eius odio in accusantium similique pariatur iste quod vero? Veritatis officia, quo magnam placeat magni reprehenderit voluptate dolore accusantium esse corrupti saepe. Sunt consequuntur officia corporis earum error doloremque tenetur accusamus'
    db.session.commit()
    return None

@client.route('/add-glossary-pair')
def addGlossary():
    num = session.get('glossary-pairs')
    if (num<10):
        session['glossary-pairs'] = num+1
    return redirect(url_for('client.home'))

"""
A route for allow new glossaryEntries to be added to the database while the form is being processed for the transaltion request
The create translation form
"""
# @client.route('/add_glossary_pair',methods=['POST'])
# def add_glossary_pair():
#     sourceText = request.form['sourceText']
#     targetText= request.form['targetText']
#     glossaryPair = GlossaryPair(sourceText=sourceText, targetText=targetText)
#     db.session.add(glossaryPair)
#     db.session.commit()
#     #where do we go after this? May need to add another one
#     return gettext("Glossary Pair submitted successfully!")