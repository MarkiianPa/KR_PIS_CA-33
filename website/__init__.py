from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager

db = SQLAlchemy()
DB_NAME = "database.db"
def create_app():
    app = Flask(__name__, static_folder="static", static_url_path="/website/static")
    app.config['SECRET_KEY'] = '1234567890'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    db.init_app(app)

    from .views import views
    from .auth import auth
    from .info import info
    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')
    app.register_blueprint(info, url_prefix='/')

    from .models import Client,Product

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)


    with app.app_context():
        db.create_all()


    @login_manager.user_loader
    def load_user(id):
        return Client.query.get(int(id))

    return app
def create_database(app):
    if not path.exists('website/' + DB_NAME):
        db.create_all(app=app)
        print('Created Database!')

