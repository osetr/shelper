from flask import (
   Flask, render_template, redirect,
   url_for, request, make_response)
from form import (
    SignUpForm, SignInForm,
    NewExForm, NewTrainForm,
    FeedbackForm, ConfirmDeletingForm)
from flask_jwt_extended import (
    jwt_required,
    jwt_refresh_token_required,
    get_raw_jwt)
from app import app, jwt
import crud

if __name__ == ' __main__':
    app.run()


@jwt.revoked_token_loader
def token_revoked():
    return redirect(url_for('index'))


@jwt.token_in_blacklist_loader
def check_if_token_in_blacklist(decrypted_token):
    return crud.CheckIfTokenInBlacklist(decrypted_token)


@jwt.expired_token_loader
def my_expired_token_callback(expired_token):
    if expired_token['type'] == 'access':
        return redirect(url_for('refresh'))
    return redirect(url_for('index'))


@app.route('/', methods=['GET', 'POST'])
def index():
    form = SignInForm()
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
    form = SignUpForm()
    errors = {}
    if crud.FormIsValid(form):
        if crud.UserExists():
            errors = {'LoginError': ['Login already in use.']}
        else:
            crud.AddUserToDataBase()
            return redirect(url_for('index'))
    elif not form.validate() and form.is_submitted():
        errors = form.errors
    return render_template('signup.html', form=form, errors=errors)


@app.route('/home', methods=['GET', 'POST'])
@app.route('/home/<user_exit>', methods=['GET', 'POST'])
@jwt_required
def main(user_exit=False):
    form_ex = NewExForm()
    form_train = NewTrainForm()
    form_feedback = FeedbackForm()
    if user_exit:
        crud.AddTokenToBlacklist()
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
    csrf_token = (get_raw_jwt() or {}).get("csrf")
    response = make_response(render_template('home.html',
                                             form_feedback=form_feedback,
                                             form_ex=form_ex,
                                             form_train=form_train,
                                             ex_list=ex_list,
                                             csrf_token=csrf_token))
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
    form_confirm_deleting = ConfirmDeletingForm()
    all_exercises = crud.GetExerciseList()
    all_trainings = crud.GetTrainingList()
    if sorted_by == "by_exname":
        all_exercises_sorted = crud.SortExercises(exercises=all_exercises,
                                                  by="exercise_name")
    elif sorted_by == "by_datetime":
        all_exercises_sorted = crud.SortExercises(exercises=all_exercises,
                                                  by="date_time")
    else:
        all_exercises_sorted = crud.SortExercises(exercises=all_exercises)
    if form_confirm_deleting.is_submitted():
        crud.DeleteSelectedExercises()
        return redirect(url_for('show'))
    csrf_token = (get_raw_jwt() or {}).get("csrf")
    response = make_response(render_template(
                                'show.html',
                                all_exercises_sorted=all_exercises_sorted,
                                all_trainings=all_trainings,
                                form=form_confirm_deleting,
                                sorted_by=sorted_by,
                                csrf_token=csrf_token))
    response.set_cookie(key='current_page',
                        value='show')
    return response


@app.route('/refresh', methods=['GET'])
@jwt_refresh_token_required
def refresh():
    current_page = request.cookies.get('current_page')
    response = make_response(redirect(url_for(current_page)))
    response.set_cookie(key='access_token_cookie',
                        value=crud.GetAccessToken(id_already_authorized=True))
    return response
