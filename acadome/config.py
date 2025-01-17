import os
from dotenv import load_dotenv

load_dotenv(os.path.join(os.path.dirname(__file__), '.env'))

class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY")
    FLASK_APP = 'wsgi.py'
    STATIC_FOLDER = 'static'
    TEMPLATES_FOLDER = 'templates'
    MONGODB_HOST = os.environ.get("MONGODB_HOST")
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 587
    MAIL_USERNAME = os.environ.get("MAIL_USERNAME")
    MAIL_PASSWORD = os.environ.get("MAIL_PASSWORD")
    MAIL_USE_TLS = True
