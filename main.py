from flask import Flask
from flask import (
render_template, session, redirect,
url_for, request, make_response
)
from app import app, db
from form import (
SignUpForm, SignInForm,
NewExForm, NewTrainForm,
FeedbackForm, ConfirmDeletingForm
)
import crud
import pymysql
from flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token,
    jwt_refresh_token_required, create_refresh_token,
    get_jwt_identity, get_raw_jwt
)
from app import jwt, blacklist
from datetime import datetime, timedelta

pymysql.install_as_MySQLdb()

if __name__ ==' __main__':
    app.run()

db.create_all()


@jwt.token_in_blacklist_loader
def check_if_token_in_blacklist(decrypted_token):
    jti = decrypted_token['jti']
    return jti in blacklist

@jwt.expired_token_loader
def my_expired_token_callback(expired_token):
    if expired_token['type'] == 'access':
        return redirect(url_for('refresh'))
    return redirect(url_for('index'))

@app.route('/', methods=['GET', 'POST'])
def index():
    form=SignInForm()
    errors = {}
    if crud.FormIsValid(form):
        if crud.UserExists() and crud.UserFilledInCorrectData():
            response = make_response(redirect(url_for('main')))
            response.set_cookie(key='access_token_cookie',
                                value=crud.GetAccessToken())
            response.set_cookie(key='refresh_token_cookie',
                                value=crud.GetRefreshToken())
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
@app.route('/home/<user_exit>', methods=['GET', 'POST'])
@jwt_required
def main(user_exit=False):
    form_ex = NewExForm()
    form_train = NewTrainForm()
    form_feedback = FeedbackForm()
    if user_exit:
        jti = get_raw_jwt()['jti']
        blacklist.add(jti)
        return redirect(url_for('index'))
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
    response = make_response(render_template('home.html', form_feedback=form_feedback,
                                        form_ex=form_ex,
                                        form_train=form_train,
                                        ex_list=ex_list,
                                        csrf_token=(get_raw_jwt() or {}).get("csrf")))
    response.set_cookie(key='current_page',
                        value='main')
    return response

@app.route('/stopwatch', methods=['GET', 'POST'])
def stopwatch():
    return render_template('stopwatch.html')


@app.route('/show', methods=['GET', 'POST'])
@app.route('/show/<sorted_by>', methods=['GET', 'POST'])
@jwt_required
def show(sorted_by=None):
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
    response = make_response(render_template('show.html', all_exercises=all_exercises,
                                        all_trainings=all_trainings,
                                        form=form,
                                        sorted_by=sorted_by,
                                        csrf_token=(get_raw_jwt() or {}).get("csrf")))
    response.set_cookie(key='current_page',
                        value='show')
    return response

@app.route('/refresh', methods=['GET'])
@jwt_refresh_token_required
def refresh():
    response = make_response(redirect(url_for(request.cookies.get('current_page'))))
    response.set_cookie(key='access_token_cookie',
                        value=crud.GetAccessToken(id_already_authorized=True))
    return response
