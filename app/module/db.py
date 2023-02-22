from flask_sqlalchemy import SQLAlchemy
from flask import Flask
db = SQLAlchemy()

def initDB(app):

    user = 'developer'
    host = '0.0.0.0'
    # host = 'mysql-server'
    port = 3306
    password = 'password'
    database = 'maindb'
    # app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://developer:password@127.0.0.1:3306/maindb'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+pymysql://{user}:{password}@{host}:{port}/{database}'
    app.config['SECRET_KEY'] = 'mySecretKey'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False # silence the deprecation warning

    db.init_app(app)


class User(db.Model):
    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_email = db.Column(db.String(100), unique=True, nullable=False)
    user_password = db.Column(db.String(150), nullable=False)

class Video(db.Model):
    video_id    = db.Column(db.Integer, primary_key=True, autoincrement=True)
    video_name  = db.Column(db.String(100), unique=True, nullable=False)
    video_url   = db.Column(db.String(150), unique=True, nullable=False)
    video_owner = db.Column(db.Integer, nullable=False)
    srt_url     = db.Column(db.String(150), unique=True, nullable=True)
    is_converted    = db.Column(db.Boolean, default=False)


def addUser(user):
    db.session.add(user)
    db.session.commit()

def addVideo(video):
    db.session.add(video)
    db.session.commit()

def updateVideo():
    db.session.commit()



# if __name__ == '__main__':
    # app = Flask(__name__)
    # initDB(app)
    # with app.app_context():
    #     db.create_all()
    #     user = User(   
    #         user_email = 'sam@123',
    #         user_password = 'sam'
    #     )
    #     addUser(user)