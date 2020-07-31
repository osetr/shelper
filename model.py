from app import db
import pymysql
import datetime

pymysql.install_as_MySQLdb()


class User(db.Model):
    __tablename__ = "clients"

    id = db.Column(db.String(40), primary_key=True)
    login = db.Column(db.String(15), unique=True, nullable=False)
    email = db.Column(db.String(120), nullable=False)
    hashed_password = db.Column(db.Text, nullable=False)
    exercises = db.relationship('Exercises',
                                backref=db.backref('user', lazy=True))
    trainings = db.relationship('Trainings',
                                backref=db.backref('user', lazy=True))
    feedbacks = db.relationship('Feedbacks',
                                backref=db.backref('user', lazy=True))

    def __repr__(self):

        return '<User %r>' % self.id


class Exercises(db.Model):
    __tablename__ = "exercises"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.String(40),
                        db.ForeignKey('clients.id'),
                        nullable=False)
    date_time = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    muscules_type = db.Column(db.String(20), nullable=False)
    exercise_name = db.Column(db.String(40), nullable=False)

    def __repr__(self):
        return '<Exercise %r>' % self.id


class Trainings(db.Model):
    __tablename__ = "trainings"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    training_id = db.Column(db.String(40), nullable=False)
    user_id = db.Column(db.String(40),
                        db.ForeignKey('clients.id'),
                        nullable=False)
    comment = db.Column(db.String(40))
    date = db.Column(db.Date, nullable=False)
    weight = db.Column(db.Integer)
    exercise_name = db.Column(db.String(40), nullable=False)
    exercise_weight = db.Column(db.Integer, default="-")

    def __repr__(self):
        return '<Training %r>' % self.training_id


class Feedbacks(db.Model):
    __tablename__ = "feedbacks"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.String(40),
                        db.ForeignKey('clients.id'),
                        nullable=False)
    text = db.Column(db.Text)

    def __repr__(self):
        return '<Feedback %r>' % self.user_id
