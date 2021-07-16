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

from acadome.gen import gen
from acadome.admin import admin
from acadome.articles import articles
from acadome.users import users
from acadome.errors import errors
app.register_blueprint(admin)
app.register_blueprint(articles)
app.register_blueprint(gen)
app.register_blueprint(users)
app.register_blueprint(errors)
