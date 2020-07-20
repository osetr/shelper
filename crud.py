from model import User, Exercises
from app import db
from passlib.context import CryptContext
from flask import session, request, jsonify
from flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token,
    get_jwt_identity
)
import uuid

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
    user_id = 1
    db.session.add(Exercises(user_id=user_id,
                             muscules_type=category,
                             exercise_name=name))
    db.session.commit()
    return 0;

def AuthUser():
    access_token = create_access_token(identity=request.form['name'])
    return jsonify(access_token=access_token), 200

def UserExists():
    return User.query.filter_by(login=request.form['name']).first()

def UserFilledInCorrectData():
    login = request.form['name']
    password = request.form['password']
    hashed_password = User.query.filter_by(login=login).first().hashed_password
    return pwd_context.verify(password, hashed_password)
