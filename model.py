from app import db
import pymysql

pymysql.install_as_MySQLdb()

class User(db.Model):
    __tablename__ = "clients"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    login = db.Column(db.String(15), unique=True, nullable=False)
    email = db.Column(db.String(120), nullable=False)
    hashed_password = db.Column(db.Text)

    def __repr__(self):
        return '<User %r>' % self.username

db.create_all()
