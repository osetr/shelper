from flask import Flask
from flask import render_template, session, redirect, url_for
from flask_wtf import Form
from wtforms import StringField, SubmitField, PasswordField
from wtforms import validators
from wtforms.validators import Required, Email, Length, Regexp

app = Flask(__name__)
app.config["SECRET_KEY"] = "key"


class AuthForm(Form):
    name = StringField("Username", validators=[Required(), Length(min=5, max=15, message='Username field must be 5-15 characters long.')])
    password = PasswordField("Password",  validators=[Required(), Regexp(regex=r'[A-Za-z0-9@#$%^&+=]{8,}', message="Easy password")])
    email = StringField("Email",  validators=[Required(), Email()])
    submit = SubmitField("Submit")
    reset = SubmitField("Reset")

class SignInForm(Form):
        name = StringField("", validators=[Required()])
        password = PasswordField("",  validators=[Required()])
        submit = SubmitField("Login")


if __name__ ==' __main__':
    app.run(debug=True)

@app.route('/')
def index():
    form=SignInForm()
    if form.validate_on_submit() and form.is_submitted():
        return 'gg'
    return render_template('index.html', form=form)

@app.route('/auth', methods=['GET', 'POST'])
def auth():
    form=AuthForm()
    errors={}
    if form.validate_on_submit() and form.is_submitted():
        return redirect(url_for('auth'))
    elif not form.validate_on_submit() and form.is_submitted():
        return render_template('auth.html', form=form, errors=form.errors)
    return render_template('auth.html', form=form, errors=errors)
