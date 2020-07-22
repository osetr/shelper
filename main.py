from flask import Flask
from flask import render_template, session, redirect, url_for, request, make_response
from app import app, db
from form import SignUpForm, SignInForm, NewExForm, NewTrainForm
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
    if crud.FormIsValid(form):
        if crud.UserExists() and crud.UserFilledInCorrectData():
            response = make_response(redirect(url_for('main')))
            response.set_cookie('access_token', crud.GetAccessToken())
            return response
        else:
             errors = {'LoginError': ["Failed login or password."]}
    return render_template('index.html', form=form, errors=errors)


@app.route('/signup', methods=['GET', 'POST'])
def auth():
    form=SignUpForm()
    errors = {}
    if crud.FormIsValid(form):
        if crud.UserExists():
            errors = {'LoginError': ['Login already in use.']}
        else:
            crud.AddUserToDataBase()
            return redirect(url_for('index'))
    elif not crud.FormIsValid(form):
        return render_template('signup.html', form=form, errors=form.errors)
    return render_template('signup.html', form=form, errors=errors)


@app.route('/home', methods=['GET', 'POST'])
def main():
    try:
        crud.CheckAccessToken()
    except:
        return "soory"
    form_ex = NewExForm()
    form_train = NewTrainForm()
    if crud.FormIsValid(form_ex):
        crud.AddExerciseToDataBase()
        return redirect(url_for('main'))
    ex_list = crud.GetExerciseList()
    return render_template('home.html', form_ex=form_ex, form_train=form_train, ex_list=ex_list)
