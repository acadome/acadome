import re
from wtforms import Form, StringField, TextAreaField, SelectField
from wtforms.validators import ValidationError

def required(form, field):
    if not field.data:
        raise ValidationError()

def length(min=0, max=256):
    if min:
        msg = f'Must be between {min} and {max} characters.'
    else:
        msg = f'Cannot exceed {max} characters.'
    def _length(form, field):
        if len(field.data) < min or len(field.data) > max:
            raise ValidationError(msg)
    return _length

def regex(r):
    def _regex(form, field):
        msg = f'Invalid characters in {field.name}.'
        if not re.match(r, field.data):
            raise ValidationError(msg)
    return _regex

class EditArticleForm(Form):
    title = StringField('Title *', validators=[
        required,
        length,
        regex('[\s\S]+'),
    ])
    authors = StringField('Author(s)', validators=[
        length,
        regex('^[a-zA-Z \-\'\,]*$'),
    ])
    abstract = TextAreaField('Abstract *', validators=[
        required,
        length(max=1024),
        regex('[\s\S]+'),
    ])
    keywords = StringField('Keywords *', validators=[
        required,
        length(min=5, max=256),
        regex('[\s\S]+'),
    ])
    field = SelectField('Field *', choices=[
        'Physics',
        'Mathematics',
    ])
    reviewers = StringField('Peer reviewers', validators=[
        length,
        regex('[\s\S]*')
    ])
