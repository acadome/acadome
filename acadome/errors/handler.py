from flask import render_template
from werkzeug.exceptions import HTTPException
from acadome.errors import errors

@errors.app_errorhandler(HTTPException)
def error_404(error):
    return render_template(
        'error.html',
        title=error.name,
        error=error
    ), error.code
