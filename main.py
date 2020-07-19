from flask import Flask
from flask import render_template, session, redirect, url_for, request
from app import app, db
from form import SignUpForm, SignInForm
import crud
import pymysql
pymysql.install_as_MySQLdb()


if __name__ ==' __main__':
    app.run()


db.create_all()


@app.route('/', methods=['GET', 'POST'])
def index():
    form=SignInForm()
    errors = {}
    if crud.FormIsValid(form) and crud.UserExists():
        return crud.AuthUser()
    elif crud.FormIsValid(form):
        errors = {'LoginError': ["User doesn't exist."]}
    return render_template('index.html', form=form, errors=errors)


@app.route('/signup', methods=['GET', 'POST'])
def auth():
    form=SignUpForm()
    errors = {}
    if crud.FormIsValid(form):
        try:
            crud.AddUserToDataBase()
            return redirect(url_for('index'))
        except:
            errors = {'LoginError': ['Login already in use.']}
    elif not crud.FormIsValid(form):
        return render_template('signup.html', form=form, errors=form.errors)
    return render_template('signup.html', form=form, errors=errors)


@app.route('/home', methods=['GET', 'POST'])
def main():
    return render_template('home.html', exercise_list=['Arms','Legs','Back','Chest','Neck','Abs','Other'])
