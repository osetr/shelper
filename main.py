from flask import Flask
from flask import render_template, session, redirect, url_for, request, make_response
from app import app, db
from form import SignUpForm, SignInForm, NewExForm, NewTrainForm, FeedbackForm, ConfirmDeletingForm
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
    elif not form.validate() and form.is_submitted():
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
    form_feedback = FeedbackForm()
    if form_ex.name.data and form_ex.is_submitted():
        crud.AddExerciseToDataBase()
        return redirect(url_for('main'))
    if form_feedback.text.data and form_feedback.is_submitted():
        crud.AddFeedbackToDataBase()
        return redirect(url_for('main'))
    if form_train.date.data and form_train.is_submitted():
        crud.AddTrainingToDataBase()
        return redirect(url_for('main'))
    ex_list = crud.GetExerciseList()
    return render_template('home.html', form_feedback=form_feedback,
                                        form_ex=form_ex,
                                        form_train=form_train,
                                        ex_list=ex_list)


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
