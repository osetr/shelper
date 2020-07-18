from flask import Flask
from flask import render_template, session, redirect, url_for, request
from model import User
from app import app, db
from form import AuthForm, SignInForm
import pymysql
pymysql.install_as_MySQLdb()


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
        db.session.add(User(login=request.form['name'], email=request.form['email'], hashed_password=request.form['password']))
        db.session.commit()
        return redirect(url_for('auth'))
    elif not form.validate_on_submit() and form.is_submitted():
        return render_template('auth.html', form=form, errors=form.errors)
    return render_template('auth.html', form=form, errors=errors)
