from flask import Flask
from flask import render_template, session, redirect, url_for, request, make_response
from app import app, db
from form import SignUpForm, SignInForm, NewExForm, NewTrainForm, FeedbackForm, ConfirmDeletingForm
import crud
import pymysql
from flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token,
    jwt_refresh_token_required, create_refresh_token,
    get_jwt_identity
)

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
            response.set_cookie('access_token_cookie', crud.GetAccessToken())
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
    elif not form.validate() and form.is_submitted():
        return render_template('signup.html', form=form, errors=form.errors)
    return render_template('signup.html', form=form, errors=errors)


@app.route('/home', methods=['GET', 'POST'])
@jwt_required
def main():
    return {"cur_user": get_jwt_identity()}


@app.route('/stopwatch', methods=['GET', 'POST'])
def stopwatch():
    return render_template('stopwatch.html')


@app.route('/show', methods=['GET', 'POST'])
@app.route('/show/<sorted_by>', methods=['GET', 'POST'])
def show(sorted_by=None):
    try:
        crud.CheckAccessToken()
    except:
        return "soory"
    form = ConfirmDeletingForm()
    all_exercises = crud.GetExerciseList()
    all_trainings = crud.GetTrainingList()
    if sorted_by=="by_exname":
        all_exercises = crud.SortExercises(exercises=all_exercises,
                                           by="exercise_name")
    elif sorted_by=="by_datetime":
        all_exercises = crud.SortExercises(exercises=all_exercises,
                                           by="date_time")
    else:
        all_exercises = crud.SortExercises(exercises=all_exercises)
    if form.is_submitted():
        crud.DeleteSelectedExercises()
        return redirect(url_for('show'))
    return render_template('show.html', all_exercises=all_exercises,
                                        all_trainings=all_trainings,
                                        form=form,
                                        sorted_by=sorted_by)
