import os
from flask import Flask
from flask_login import LoginManager
from .models import init_db, User
from dotenv import load_dotenv


load_dotenv()


def create_app():
app = Flask(__name__, instance_relative_config=True)
app.config['SECRET_KEY'] = os.getenv('FLASK_SECRET_KEY', 'dev-secret')
app.config['DATABASE_URL'] = os.getenv('DATABASE_URL', 'sqlite:///../instance/app.sqlite')


# ensure instance folder exists
try:
os.makedirs(app.instance_path, exist_ok=True)
except Exception:
pass


# initialize DB (simple sqlite)
init_db(app)


login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
return User.get_by_id(user_id)


# register blueprints
from .auth import auth_bp
from .routes import main_bp


app.register_blueprint(auth_bp)
app.register_blueprint(main_bp)


return app