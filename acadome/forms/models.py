import os
import re
from flask import request
from wtforms import Form, StringField, TextAreaField, SelectField, PasswordField, FileField, MultipleFileField, BooleanField
from wtforms.validators import ValidationError
from acadome import db, um, bcrypt

def required(form, field):
    if not field.data:
        raise ValidationError('')

def length(min=0, max=256):
    if min:
        msg = f'Must be between {min} and {max} characters.'
    else:
        msg = f'Cannot exceed {max} characters.'
    def _length(form, field):
        if len(field.data) < min or len(field.data) > max:
            raise ValidationError(msg)
    return _length

def regex(r='[\s\S]*'):
    def _regex(form, field):
        if field.name == 'email':
            msg = 'Invalid email address.'
        elif field.name == 'password':
            msg = 'Allowed characters: a-z, A-Z, 0-9, and _.'
        else:
            msg = f'Invalid characters in {field.name}.'
        if not re.match(r, field.data):
            raise ValidationError(msg)
    return _regex

class JSForm(Form):
    js = BooleanField()

# ARTICLES
def file_required(form, field):
    file = request.files.getlist(field.name)
    for f in file:
        if not f.filename:
            raise ValidationError()

def formats(exts):
    def _formats(form, field):
        file = request.files.getlist(field.name)
        for f in file:
            _, ext = os.path.splitext(f.filename)
            if ext.lower() not in exts:
                raise ValidationError('Invalid file type.')
    return _formats

def size(mb=5):
    max = mb*1024*1024
    def _size(form, field):
        file = request.files.getlist(field.name)
        for f in file:
            if len(f.read()) > max:
                raise ValidationError(f'File size exceeds {mb}MB limit.')
    return _size

class BaseArticle():
    def __init__(self):
        self.title = [
            required,
            length(),
            regex(),
        ]
        self.authors = [
            length(),
            regex(),
        ]
        self.abstract = [
            required,
            length(),
            regex(),
        ]
        self.keywords = [
            required,
            length(),
            regex(),
        ]
        self.fields = [
            f['name'] for f in db.fields.find().sort([('name', 1)])
        ]
        self.reviewers = [
            length(),
            regex(),
        ]

class PublishForm(JSForm):
    val = BaseArticle()
    title = StringField('Title *', val.title)
    authors = StringField('Co-author(s)', val.authors)
    abstract = TextAreaField('Abstract *', val.abstract)
    keywords = StringField('Keywords *', val.keywords)
    field = SelectField('Field *', choices=val.fields)
    preprint = FileField('Preprint', [
        file_required,
        formats(['.pdf']),
        size(),
    ])
    images = MultipleFileField('Images', [
        file_required,
        formats(['.jpg', '.png']),
        size(),
    ])
    reviewers = StringField('Peer reviewer suggestions', val.reviewers)
    pa = BooleanField('Publishing agreement', [required])

class EditArticleForm(JSForm):
    val = BaseArticle()
    title = StringField('Title *', val.title)
    val.authors.append(required)
    authors = StringField('Author(s)', val.authors)
    abstract = TextAreaField('Abstract *', val.abstract)
    keywords = StringField('Keywords *', val.keywords)
    field = SelectField('Field *', choices=val.fields)
    reviewers = StringField('Peer reviewers', val.reviewers)

# USERS
def unique(form, field):
    if db.users.find_one({'email': field.data}):
        if um.user and field.data == um.user['email']:
            pass
        else:
            raise ValidationError('Already exists in our database.')

def verified(form, field):
    user = db.users.find_one({'email': field.data})
    if user:
        if not user['verified']:
            raise ValidationError('Account not yet verified.')
    else:
        raise ValidationError('Does not exist in our database.')

def check_password(form, field):
    email = um.user['email'] if um.user else form.email.data
    user = db.users.find_one({'email': email})
    if user:
        if not bcrypt.check_password_hash(user['password'], field.data):
            raise ValidationError('Incorrect password.')

class BaseUser:
    def __init__(self):
        self.name = [
            required,
            length(min=3, max=64),
            regex('^[a-zA-Z \-\']+$'),
        ]
        self.affil = [
            length(max=256),
            regex('^[a-zA-Z0-9 \,\.\-\']*$'),
        ]
        self.email = [
            required,
            length(min=5, max=254),
            regex('^\S+@\S+\.\S+$'),
        ]
        self.password = [
            required,
            length(min=8, max=64),
            regex('^[a-zA-Z0-9!@#$%^&*_]+$'),
        ]

class SignUpForm(JSForm):
    val = BaseUser()
    name = StringField('Name *', val.name)
    affiliation = StringField('Affiliation', val.affil)
    val.email.append(unique)
    email = StringField('Email address *', val.email)
    password = PasswordField('Password *', val.password)
    ua = BooleanField('User agreement', [required])

class LoginForm(JSForm):
    val = BaseUser()
    val.email.append(verified)
    email = StringField('Email address', val.email)
    val.password.append(check_password)
    password = PasswordField('Password', val.password)

class EditAccountForm(JSForm):
    val = BaseUser()
    name = StringField('Name *', val.name)
    affiliation = StringField('Affiliation', val.affil)
    val.email.append(unique)
    email = StringField('Email address *', val.email)
    val.password.append(check_password)
    password = PasswordField('Enter password to confirm changes *', val.password)

class RequestResetForm(JSForm):
    val = BaseUser()
    val.email.append(verified)
    email = StringField('Email address', val.email)

class ResetPasswordForm(JSForm):
    val = BaseUser()
    password = PasswordField('New password', val.password)

class DeleteForm(JSForm):
    val = BaseUser()
    email = StringField('Email address', val.email)
    val.password.append(check_password)
    password = PasswordField('Password', val.password)

# GENERAL
class ContactForm(JSForm):
    val = BaseUser()
    name = StringField('Name', val.name)
    email = StringField('Email', val.email)
    query = TextAreaField('Query', validators=[
        required,
        length(),
        regex(),
    ])
