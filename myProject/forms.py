from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,SubmitField,ValidationError,SelectField,RadioField,TextAreaField,IntegerField,DecimalField,DateTimeField
from wtforms.validators import DataRequired,Email,EqualTo
from myProject.models import Client,Translator
from datetime import datetime
import pytz

def check_email_client(form, field):
    if Client.query.filter_by(email=field.data).first():
        raise ValidationError('Email already registered.')

def check_email_translator(form, field):
    if Translator.query.filter_by(email=field.data).first():
        raise ValidationError('Email already registered.')
        

def languageNotEqualTo(form,field):
    if field.data == form.language_from.data:
        raise ValidationError('These fields can not be the same.')

class LoginForm(FlaskForm):
    email = StringField('Email',validators=[DataRequired(),Email()])
    password = PasswordField('Password',validators=[DataRequired()])
    submit = SubmitField('Login')


class RegisterationForm(FlaskForm):
    name = StringField('Name',validators=[DataRequired()])
    email = StringField('Email',validators=[DataRequired(),Email()])
    password = PasswordField('Password',validators=[DataRequired(),EqualTo('pass_confirm')])
    pass_confirm = PasswordField('Confirm Password',validators=[DataRequired()])
    submit = SubmitField('Register')

class ForgotPassForm(FlaskForm):
    email = StringField('Email',validators=[DataRequired(),Email()])
    submit = SubmitField('Get Reset Link')

class ChangePassForm(FlaskForm):
    password = PasswordField('Password',validators=[DataRequired(),EqualTo('pass_confirm')])
    pass_confirm = PasswordField('Confirm Password',validators=[DataRequired()])
    submit = SubmitField('Register')

class TranslationForm(FlaskForm):
    berlin_tz = pytz.timezone("Europe/Berlin")
    time_now  = datetime.now(berlin_tz).strftime("%d %M %Y %H:%M")
    possibleDeadlines = [30,60,90,240]
    deadlineChoices = list(map(lambda x: str(x)+ " minutes from your Submit", possibleDeadlines))
    
    language_from = SelectField("From",choices=[('english','English'),('german','German'),("russian","Russian")],default="german", validators=[DataRequired()])
    language_to = SelectField("To",choices=[('english','English'),('german','German'),("russian","Russian")],default="english", validators=[DataRequired(),languageNotEqualTo])
    deadline = RadioField("Deadline",choices=deadlineChoices,validators=[DataRequired()])
    rejectCriteria = RadioField('Reject Criteria',choices=[(1,"Reject"),(2,"50% Discount"),(3,"No Action")],default=1, validators=[DataRequired()])
    text = TextAreaField("Source text",validators=[DataRequired()])
    submit = SubmitField('editPrice')

class GetPriceForm(FlaskForm):
    price = IntegerField("Price",validators=[DataRequired()])
    submit = SubmitField('Make Request')

class RegisterTranslator(FlaskForm):
    name = StringField('Name',validators=[DataRequired()])
    email = StringField('Email',validators=[DataRequired(),Email()])
    password = PasswordField('Password',validators=[DataRequired(),EqualTo('pass_confirm')])
    pass_confirm = PasswordField('Confirm Password',validators=[DataRequired()])
    submit = SubmitField('Register')

class AddServiceForm(FlaskForm):
    language_from = SelectField("From",choices=[('english','English'),('german','German'),("russian","Russian")],validators=[DataRequired()])
    language_to = SelectField("To",choices=[('english','English'),('german','German'),("russian","Russian")],validators=[DataRequired(),languageNotEqualTo])
    min_price = IntegerField("Min Price",validators=[DataRequired()])
    target_price = IntegerField("Target Price",validators=[DataRequired()])
    deadline = RadioField("Deadline",choices=[(1,"30 minutes"),(2,"60 minutes"),(3,"90 minutes"),(4,"120 minutes")],validators=[DataRequired()])
    submit = SubmitField('Add Service')

class SubmitTranslationForm(FlaskForm):
    translation = TextAreaField("Translation",validators=[DataRequired()])
    submit = SubmitField('Submit')