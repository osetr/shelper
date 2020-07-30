from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
import pymysql
from flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token,
    jwt_refresh_token_required, create_refresh_token,
    get_jwt_identity
)
import redis

pymysql.install_as_MySQLdb()

app = Flask(__name__)

app.config["SECRET_KEY"] = "key"
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:uawesome120300@127.0.0.1:3306/shelper'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['JWT_SECRET_KEY'] = 'super-secret'
app.config['JWT_TOKEN_LOCATION'] = ['cookies']
app.config['JWT_COOKIE_CSRF_PROTECT'] = True
app.config['JWT_CSRF_CHECK_FORM'] = True
app.config['JWT_BLACKLIST_ENABLED'] = True
jwt = JWTManager(app)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
revoked_store = redis.StrictRedis(host='localhost', port=6379, db=0,
                                  decode_responses=True)
