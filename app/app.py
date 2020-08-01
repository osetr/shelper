from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
import redis
import pymysql
from dotenv import load_dotenv, find_dotenv
import os

load_dotenv(find_dotenv())

pymysql.install_as_MySQLdb()

app = Flask(__name__)

app.config["SECRET_KEY"] = os.getenv("SECRET_CSRF_KEY")
app.config['SQLALCHEMY_DATABASE_URI'] = (
    'mysql://root:' +
    os.getenv("DB_PASSWORD") +
    '@127.0.0.1:3306/shelper')
app.config['JWT_SECRET_KEY'] = os.getenv("JWT_SECRET_KEY")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['JWT_TOKEN_LOCATION'] = ['cookies']
app.config['JWT_COOKIE_CSRF_PROTECT'] = True
app.config['JWT_CSRF_CHECK_FORM'] = True
app.config['JWT_BLACKLIST_ENABLED'] = True
jwt = JWTManager(app)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
revoked_store = redis.StrictRedis(host='localhost', port=6379, db=0,
                                  decode_responses=True)
types_muscle = ['Other', 'Arms', 'Legs', 'Back', 'Chest', 'Neck', 'Abs']
