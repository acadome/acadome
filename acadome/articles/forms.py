import os
import re
from flask import request
from wtforms import Form, StringField, TextAreaField, BooleanField, FileField
from wtforms.validators import ValidationError
from acadome import db, um, bcrypt

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

def format(form, field):
    file = request.files[field.name]
    _, ext = os.path.splitext(file.filename)
    if ext.lower() != '.pdf':
        raise ValidationError('Invalid file type. Please upload a PDF.')

class PublishForm(Form):
    title = StringField('Title *', validators=[
        required,
        length(max=256),
        regex('[\s\S]+'),
    ])
    authors = StringField('Co-author(s)', validators=[
        length(max=256),
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
    file = FileField('Upload', validators=[format])
    pa = BooleanField(validators=[required])
