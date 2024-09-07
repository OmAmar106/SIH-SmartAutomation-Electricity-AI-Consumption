from flask_sqlalchemy import SQLAlchemy 
db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'User'
    ID = db.Column(db.Integer,primary_key = True,autoincrement = True)
    username = db.Column(db.String,nullable = False,unique = True)
    password = db.Column(db.String,nullable = False)
    email = db.Column(db.String,nullable = False)

class Blog(db.Model):
    __tablename__ = 'Blog'
    queryid = db.Column(db.Integer,primary_key = True,autoincrement = True)
    name = db.Column(db.String)
    query1 = db.Column(db.String)
    emailid = db.Column(db.String)