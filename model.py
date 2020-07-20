from app import db
import pymysql

pymysql.install_as_MySQLdb()

class User(db.Model):
    __tablename__ = "clients"

    id = db.Column(db.String(40), primary_key=True)
    login = db.Column(db.String(15), unique=True, nullable=False)
    email = db.Column(db.String(120), nullable=False)
    hashed_password = db.Column(db.Text, nullable=False)
    exercises = db.relationship('Exercises', backref=db.backref('user', lazy=True))

    def __repr__(self):

        return '<User %r>' % self.login

class Exercises(db.Model):
    __tablename__ = "exercises"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.String(40), db.ForeignKey('clients.id'), nullable=False)
    muscules_type = db.Column(db.String(20), nullable=False)
    exercise_name = db.Column(db.String(40), nullable=False)

    def __repr__(self):
        return '<Exercise %r>' % self.exercise_name
