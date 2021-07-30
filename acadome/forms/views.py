from flask import request
from acadome import db, um, bcrypt
from acadome.forms import forms

@forms.route('/unique_email', methods=['POST'])
def unique_email():
    email = request.get_json()['email']
    if db.users.find_one({'email': email}):
        if um.user and email == um.user['email']:
            return ''
        else:
            return 'Already exists in our database.'
    else:
        return ''

@forms.route('/verified_email', methods=['POST'])
def verified_email():
    email = request.get_json()['email']
    user = db.users.find_one({'email': email})
    if user:
        return 'Account not yet verified.' if not user['verified'] else ''
    else:
        return 'Does not exist in our database.'

@forms.route('/check_password', methods=['POST'])
def check_password():
    email = um.user['email'] if um.user else request.get_json()['email']
    user = db.users.find_one({'email': email})
    if bcrypt.check_password_hash(user['password'], request.get_json()['password']):
        return ''
    else:
        return 'Incorrect password.'
