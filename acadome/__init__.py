from flask import Flask
from pymongo import MongoClient
from flask_mail import Mail
from acadome.config import Config

app = Flask(__name__)
app.config.from_object(Config)
client = MongoClient(app.config['MONGODB_HOST'], connect=False)
db = client.acadome_db
mail = Mail(app)

from acadome.gen import gen
from acadome.articles import articles
from acadome.errors import errors
app.register_blueprint(gen)
app.register_blueprint(articles)
app.register_blueprint(errors)
