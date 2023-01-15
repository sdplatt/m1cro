from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,SubmitField,ValidationError,SelectField,RadioField,TextAreaField,IntegerField
from wtforms.validators import DataRequired,Email,EqualTo,Length
from myProject.models import Client

def check_email(form, field):
    if Client.query.filter_by(email=field.data).first():
        raise ValidationError('Email already registered.')

class LoginForm(FlaskForm):
    email = StringField('Email',validators=[DataRequired(),Email()])
    password = PasswordField('Password',validators=[DataRequired()])
    submit = SubmitField('Login')


class RegisterationForm(FlaskForm):
    name = StringField('Name',validators=[DataRequired()])
    email = StringField('Email',validators=[DataRequired(),Email(),check_email])
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
    language_from = SelectField("From",choices=[('english','English'),('german','German'),("russian","Russian")],validators=[DataRequired()])
    language_to = SelectField("To",choices=[('english','English'),('german','German'),("russian","Russian")],validators=[DataRequired()])
    deadline = RadioField("Deadline",choices=[(1,"next 2 hours"),(2,"Tomorrow before 9 am"),(3,"Tomorrow before 3 pm"),(4,"Day after tomorrow before 9 am")],validators=[DataRequired()])
    text = TextAreaField("Text for translation",validators=[DataRequired()])
    price = IntegerField("Your Price",validators=[DataRequired()])
    submit = SubmitField('Make Request')