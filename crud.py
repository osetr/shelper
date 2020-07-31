from model import User, Exercises, Trainings, Feedbacks
from app import db, revoked_store
from passlib.context import CryptContext
from flask import session, request, jsonify
from datetime import datetime, timedelta
import uuid
from flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token,
    jwt_refresh_token_required, create_refresh_token,
    get_jwt_identity, get_jti
)

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def FormIsValid(form):
    return form.validate() and form.is_submitted()

def AddUserToDataBase():
    login = request.form['name']
    email = request.form['email']
    hashed_password = pwd_context.hash(request.form['password'])
    db.session.add(User(id=str(uuid.uuid4()),
                        login=login,
                        email=email,
                        hashed_password=hashed_password))
    db.session.commit()
    return 0;

def AddExerciseToDataBase():
    name = request.form['name']
    category = request.form['category']
    user_id = get_jwt_identity()
    db.session.add(Exercises(user_id=user_id,
                             muscules_type=category,
                             exercise_name=name))
    db.session.commit()
    return 0

def AddTrainingToDataBase():
    training_id = str(uuid.uuid4())
    user_id = get_jwt_identity()
    comment = request.form['comment']
    date = request.form['date']
    weight = request.form['weight']
    if weight == "":
        weight = -1
    training_list = request.form['training_list']
    exercises_list = splited_training_list = training_list.split()
    for exercise in exercises_list:
        exercise_name = (exercise.split(":"))[0]
        exercise_weight = (exercise.split(":"))[1]
        if exercise_weight == "":
            exercise_weight = 0
        db.session.add(Trainings(training_id=training_id,
                                 user_id=user_id,
                                 comment=comment,
                                 date=date,
                                 weight=weight,
                                 exercise_name= exercise_name,
                                 exercise_weight=exercise_weight))
        db.session.commit()
    return 0

def AddFeedbackToDataBase():
    user_id = get_jwt_identity()
    text = request.form['text']
    db.session.add(Feedbacks(user_id=user_id,
                             text=text))
    db.session.commit()
    return 0

def UserExists():
    return User.query.filter_by(login=request.form['name']).first()

def UserFilledInCorrectData():
    login = request.form['name']
    password = request.form['password']
    hashed_password = User.query.filter_by(login=login).first().hashed_password
    return pwd_context.verify(password, hashed_password)

def GetAccessToken(id_already_authorized=False):
    if not id_already_authorized:
        user_id = User.query.filter_by(login=request.form['name']).first().id
    else:
        user_id = get_jwt_identity()
    access_token = create_access_token(
    identity=user_id,
    expires_delta=timedelta(minutes=180),
    headers={'User-Agent': request.headers['User-Agent']}
    )
    return access_token

def GetRefreshToken():
    user_id = get_jwt_identity()
    refresh_token = create_refresh_token(
    identity=user_id,
    expires_delta=timedelta(days=1),
    headers={'User-Agent': request.headers['User-Agent']}
    )
    return refresh_token

def CheckAccessToken():
    token = request.cookies.get('access_token')
    jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

def GetExerciseList():
    user_id = get_jwt_identity()
    dict = {}
    for muscules_type in ['Arms','Legs','Back','Chest','Neck','Abs','Other']:
        list = [
            {'name': iter.exercise_name, 'date_time': iter.date_time}
            for iter in Exercises.query.filter_by(
                user_id=user_id, muscules_type=muscules_type
            ).all()
        ]
        dict.update({muscules_type: list})
    return dict

def GetTrainingList():
    user_id = get_jwt_identity()
    list = []
    amount_of_trainings = set(iter.training_id for iter in Trainings.query.filter_by(user_id=user_id).all())
    for training_id in amount_of_trainings:
        exercises_list = []
        for single_exercise in Trainings.query.filter_by(training_id=training_id).all():
            exercises_list.append({'exercise_name':single_exercise.exercise_name, 'exercise_weight':single_exercise.exercise_weight})
        list.append({"date":single_exercise.date,"comment":single_exercise.comment,"exercises":exercises_list,"weight":single_exercise.weight})
    return sorted(list, key = lambda tr: tr['date'], reverse=True)

def DeleteSelectedExercises():
    user_id = get_jwt_identity()
    exercises_to_delete = request.form['exercise_list_to_deleting']
    exercises = exercises_to_delete.split()
    print(exercises)
    for exercise in exercises:
        db.session.delete(Exercises.query.filter_by(user_id=user_id,
                                                    exercise_name=exercise).first())
    db.session.commit()

def SortExercises(exercises, by="type_muscule"):
    exercises_list = []
    for muscules_type in exercises:
        for exercise in exercises[muscules_type]:
            exercises_list.append({'muscule_type':muscules_type,
                                   'exercise_name':exercise['name'],
                                   'date_time':exercise['date_time']})
    if by == 'exercise_name':
        return sorted(exercises_list, key = lambda ex: ex['exercise_name'])
    if by == 'date':
        return sorted(exercises_list, key = lambda ex: ex['date_time'])
    else:
        return sorted(exercises_list, key = lambda ex: ex['muscule_type'])

def AddTokenToBlacklist():
    access_token = request.cookies.get('access_token_cookie')
    access_jti = get_jti(encoded_token=access_token)
    revoked_store.set(access_jti, 'false')

def CheckIfTokenInBlacklist(decrypted_token):
    jti = decrypted_token['jti']
    entry = revoked_store.get(jti)
    if entry == 'false':
        return True
    return False
