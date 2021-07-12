import re
from wtforms import Form, StringField, PasswordField
from wtforms.validators import ValidationError
from acadome import db, um, bcrypt

def required(form, field):
    if len(field.data) == 0:
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
        if field.name == 'email':
            msg = 'Invalid email address.'
        elif field.name == 'password':
            msg = 'Allowed characters: a-z, A-Z, 0-9, and _.'
        else:
            msg = f'Invalid characters in {field.name}.'
        if not re.match(r, field.data):
            raise ValidationError(msg)
    return _regex

def unique(form, field):
    if db.users.find_one({'email': field.data}):
        if um.user and field.data == um.user['email']:
            pass
        else:
            raise ValidationError('Already exists in our database.')

def registered(form, field):
    if not db.users.find_one({'email': field.data}):
        raise ValidationError('Does not exist in our database.')

def verified(form, field):
    user = db.users.find_one({'email': field.data})
    if user:
        if not user['verified']:
            raise ValidationError('Account not yet verified.')

def check_password(form, field):
    email = um.user['email'] if um.user else form.email.data
    user = db.users.find_one({'email': email})
    if user:
        if not bcrypt.check_password_hash(user['password'], field.data):
            raise ValidationError('Incorrect password.')

class BaseVal:
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
            length(min=4, max=254),
            regex('^\S+@\S+\.\S+$'),
        ]
        self.password = [
            required,
            length(min=8, max=64),
            regex('^\w+$'),
        ]

class SignUpForm(Form):
    val = BaseVal()
    name = StringField('Name *', val.name)
    affiliation = StringField('Affiliation', val.affil)
    val.email.append(unique)
    email = StringField('Email address *', val.email)
    password = PasswordField('Password *', val.password)

class LoginForm(Form):
    val = BaseVal()
    val.email.extend([required, registered, verified])
    email = StringField('Email address', val.email)
    val.password.extend([required, check_password])
    password = PasswordField('Password', val.password)

class EditAccountForm(SignUpForm):
    val = BaseVal()
    val.password.append(check_password)
    password = PasswordField('Enter password to confirm changes *', val.password)

class ResetPasswordForm1(Form):
    val = BaseVal()
    val.email.append(registered)
    email = StringField('Email address', val.email)

class ResetPasswordForm2(Form):
    val = BaseVal()
    password = PasswordField('New password', val.password)

class DeleteForm(Form):
    val = BaseVal()
    val.password.append(check_password)
    password = PasswordField('Password', val.password)
