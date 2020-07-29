from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
import pymysql

pymysql.install_as_MySQLdb()

app = Flask(__name__)

app.config["SECRET_KEY"] = "key"
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:uawesome120300@127.0.0.1:3306/shelper'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(app)
migrate = Migrate(app, db)
