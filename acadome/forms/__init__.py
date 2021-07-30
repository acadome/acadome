from flask import Blueprint

forms = Blueprint(
    'forms',
    __name__,
    template_folder='templates',
    static_folder='static',
    static_url_path='/forms/static',
    url_prefix='/form'
)

from acadome.forms import views
