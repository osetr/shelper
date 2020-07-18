from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField
from wtforms import validators
from wtforms.validators import Required, Email, Length, Regexp


class SignUpForm(FlaskForm):
    name = StringField("Username", validators=[Required(), Length(min=5, max=15, message='Username field must be 5-15 characters long.')])
    password = PasswordField("Password",  validators=[Required(), Regexp(regex=r'[A-Za-z0-9@#$%^&+=]{8,}', message="Easy password.")])
    email = StringField("Email",  validators=[Required(), Email()])
    submit = SubmitField("Submit")
    reset = SubmitField("Reset")

class SignInForm(FlaskForm):
    name = StringField("", validators=[Required()])
    password = PasswordField("",  validators=[Required()])
    submit = SubmitField("Login")
