from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

app = Flask(__name__)

app.config['SECRET_KEY'] = '9812c2e42fc2ba86735a694f8f7ee714'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///safe_space.db'

db =SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)

from safe_space import routes