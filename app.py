from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager

app = Flask(__name__)
jwt = JWTManager(app)
db = SQLAlchemy(app)
app.config["SECRET_KEY"] = "key"
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:uawesome120300@127.0.0.1:3306/shelper'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['JWT_SECRET_KEY'] = 'super-secret'  # Change this!
