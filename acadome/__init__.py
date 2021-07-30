from flask import Flask
from pymongo import MongoClient
from flask_bcrypt import Bcrypt
from flask_mail import Mail
from acadome.config import Config
from acadome.manager import UserManager

app = Flask(__name__)
app.config.from_object(Config)

client = MongoClient(app.config['MONGODB_URI'])
db = client.acadome_db
bcrypt = Bcrypt(app)
mail = Mail(app)
um = UserManager(app)

from acadome.admin import admin
from acadome.editors import editors
from acadome.users import users
from acadome.articles import articles
from acadome.gen import gen
from acadome.forms import forms
from acadome.errors import errors
app.register_blueprint(admin)
app.register_blueprint(editors)
app.register_blueprint(users)
app.register_blueprint(articles)
app.register_blueprint(gen)
app.register_blueprint(forms)
app.register_blueprint(errors)
