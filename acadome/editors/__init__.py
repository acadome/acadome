from flask import Blueprint

editors = Blueprint(
    'editors',
    __name__,
    template_folder='templates',
    static_folder='static',
    static_url_path='/editors/static',
    url_prefix='/editors'
)

from acadome.editors import views
