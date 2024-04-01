from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String)
    email = db.Column(db.String, unique=True)
    grade = db.Column(db.String, default=0)
    userpic = db.Column(db.String)

    def __repr__(self):
        return  f"{self.username} <{self.email}>"
    

