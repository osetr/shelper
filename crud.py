from model import User, Exercises
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
    return form.validate_on_submit() and form.is_submitted()

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
    return 0;

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
    expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt
