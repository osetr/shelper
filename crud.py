from model import User, Exercises, Trainings, Feedbacks
from app import db
from passlib.context import CryptContext
from flask import session, request, jsonify
import jwt
from jwt import PyJWTError
from datetime import datetime, timedelta
import uuid

SECRET_KEY = 'asfdgfg'
ALGORITHM = 'HS256'

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
    token = request.cookies.get('access_token')
    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    user_id = payload.get("user_id")
    db.session.add(Exercises(user_id=user_id,
                             muscules_type=category,
                             exercise_name=name))
    db.session.commit()
    return 0

def AddTrainingToDataBase():
    training_id = str(uuid.uuid4())
    token = request.cookies.get('access_token')
    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    user_id = payload.get("user_id")
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
    token = request.cookies.get('access_token')
    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    user_id = payload.get("user_id")
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

def GetAccessToken():
    user_id = User.query.filter_by(login=request.form['name']).first().id
    to_encode = {'sub':request.form['name'],
                 'user_id': user_id,
                 'User-Agent':request.headers.get('User-Agent')}
    expire = datetime.utcnow() + timedelta(minutes=100)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def CheckAccessToken():
    token = request.cookies.get('access_token')
    jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

def GetExerciseList():
    token = request.cookies.get('access_token')
    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    user_id = payload.get("user_id")
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
    token = request.cookies.get('access_token')
    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    user_id = payload.get("user_id")
    list = []
    amount_of_trainings = set(iter.training_id for iter in Trainings.query.filter_by(user_id=user_id).all())
    for training_id in amount_of_trainings:
        exercises_list = []
        for single_exercise in Trainings.query.filter_by(training_id=training_id).all():
            exercises_list.append({'exercise_name':single_exercise.exercise_name, 'exercise_weight':single_exercise.exercise_weight})
        list.append({"date":single_exercise.date,"comment":single_exercise.comment,"exercises":exercises_list,"weight":single_exercise.weight})
    return sorted(list, key = lambda tr: tr['date'], reverse=True)

def DeleteSelectedExercises():
    token = request.cookies.get('access_token')
    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    user_id = payload.get("user_id")
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
