from flask import Blueprint

articles = Blueprint('articles', __name__, template_folder='templates', static_folder='static', static_url_path='/articles/static')

from . import views
