from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, SelectField, HiddenField, IntegerField, TextAreaField
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

class NewExForm(FlaskForm):
    name = StringField("Exercise's name", validators=[Required()])
    category = SelectField("Type of muscles", choices=['Other','Arms','Legs','Back','Chest','Neck','Abs'], validate_choice=False)
    submit = SubmitField("Save", id="new_exercise_submit")

class NewTrainForm(FlaskForm):
    comment = StringField("Write down comment")
    date = StringField("Date", validators=[Required()])
    weight = IntegerField("Weight")
    training_list = HiddenField("List")
    submit = SubmitField("Save", id="new_train_submit")

class FeedbackForm(FlaskForm):
    text = TextAreaField("Feedback", validators=[Required()])
    submit = SubmitField("Send", id="feedback_submit")

class ConfirmDeletingForm(FlaskForm):
    exercise_list_to_deleting = HiddenField("List")
    submit = SubmitField("confirm deleting", id="confirm_delete_button")
