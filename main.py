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
    if crud.FormIsValid(form):
        return crud.AuthUser()
    return render_template('index.html', form=form)

@app.route('/signup', methods=['GET', 'POST'])
def auth():
    form=SignUpForm()
    if crud.FormIsValid(form):
        try:
            crud.AddUserToDataBase()
            return redirect(url_for('auth'))
        except:
            errors = {'LoginError': ['Login already in use.']}
    elif not crud.FormIsValid(form):
        return render_template('auth.html', form=form, errors=form.errors)
    return render_template('auth.html', form=form, errors=errors)
