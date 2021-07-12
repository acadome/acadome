from flask import Blueprint

gen = Blueprint(
    'gen',
    __name__,
    template_folder='templates',
    static_folder='static',
    static_url_path='/gen/static'
)

from acadome.gen import views
