from flask import Flask
from flask_mongoengine import MongoEngine
from flask_mail import Mail
from acadome.config import Config

app = Flask(__name__)
app.config.from_object(Config)
db = MongoEngine(app)
mail = Mail(app)

from . import views
