from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'user_table'

    id = db.Column(db.Integer, primary_key = True)
    userId = db.Column(db.String(32), unique = True, nullable = False) #id
    nickname = db.Column(db.String(32), unique = True, nullable = False) #nickname

    def __init__(self, userId, nickname):
        self.userId = userId
        self.nickname = nickname