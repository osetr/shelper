from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
import redis
import pymysql
from dotenv import load_dotenv, find_dotenv
import os
from flask_mail import Mail

load_dotenv(find_dotenv())

pymysql.install_as_MySQLdb()

app = Flask(__name__)

app.config["SECRET_KEY"] = os.getenv("SECRET_CSRF_KEY")
app.config['SQLALCHEMY_DATABASE_URI'] = (
    'postgresql://' + os.getenv("POSTGRES_USER") +
    ':' + os.getenv("POSTGRES_PASSWORD") +
    '@localhost:5432/' + os.getenv("POSTGRES_DB"))
app.config['JWT_SECRET_KEY'] = os.getenv("JWT_SECRET_KEY")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['JWT_TOKEN_LOCATION'] = ['cookies']
app.config['JWT_COOKIE_CSRF_PROTECT'] = True
app.config['JWT_CSRF_CHECK_FORM'] = True
app.config['JWT_BLACKLIST_ENABLED'] = True
app.config['MAIL_SERVER'] = 'smtp.googlemail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = os.getenv("MAIL_USERNAME")
app.config['MAIL_DEFAULT_SENDER'] = os.getenv("MAIL_USERNAME")
app.config['MAIL_PASSWORD'] = os.getenv("MAIL_PASSWORD")
jwt = JWTManager(app)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
mail = Mail(app)
revoked_store = redis.StrictRedis(host='localhost', port=6379, db=0,
                                  decode_responses=True)
types_muscle = ['Other', 'Arms', 'Legs', 'Back', 'Chest', 'Neck', 'Abs']
