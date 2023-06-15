from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError, URL
from safe_space.models import User

class RegistrationForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm-password', validators=[DataRequired(), EqualTo('password')])
    register = SubmitField('Register')

   
    def validate_email(self, email):
        user = User.query.filter_by(name=email.data).first()
        if user:
            raise ValidationError('That email is chosen choose another')

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    login = SubmitField('Login')
class UrlForm(FlaskForm):
    url = StringField('Enter URL', validators=[DataRequired(), URL(require_tld=True, message='Please enter a valid URL (Ex. https://example.com)')])
    save = SubmitField('Save URL')


class DemoForm(FlaskForm):
    text = StringField('Sample Text to analyse', validators=[DataRequired(), Length(min=3, max=9900)])    