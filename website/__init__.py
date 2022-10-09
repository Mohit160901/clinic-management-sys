from flask import Flask
from flask_sqlalchemy import  SQLAlchemy
from os import  path
from flask_login import  LoginManager
from  flask_mail import Message,Mail


db = SQLAlchemy()

DB_NAME = "database.db"


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'njnjkbkjsdnvndkfnvnskf'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'

    #mail = Mail(app)

    #app.config['MAIL_SERVER'] = 'smtp.gmail.com'
    #app.config['MAIL_PORT'] = 465
    #app.config['MAIL_USERNAME'] = 'yourId@gmail.com'
    #app.config['MAIL_PASSWORD'] = '*****'
    #app.config['MAIL_USE_TLS'] = False
    #app.config['MAIL_USE_SSL'] = True
    #mail = Mail(app)

    db.init_app(app)





    from .views import views
    from .auth  import  auth

    app.register_blueprint(views , url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')
    
    from .models import User,Note,Doctor


    
    create_database(app)

    login_manager = LoginManager()
    login_manager.login_view = "auth.login"
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    return app


def create_database(app):
    if not path.exists('website/' + DB_NAME):
        db.create_all(app=app)
        print("Created Database")
    