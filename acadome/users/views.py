from datetime import datetime, timedelta
from flask import render_template, redirect, request, url_for, flash, abort
from flask_mail import Message
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from itsdangerous.exc import SignatureExpired
from acadome import app, db, mail, bcrypt, um
from acadome.users import users
from acadome.users.forms import SignUpForm, LoginForm, EditAccountForm, ResetPasswordForm1, ResetPasswordForm2, DeleteForm

def get_token(email, expires=300):
    s = Serializer(app.config['SECRET_KEY'], expires)
    return s.dumps({'email': email}).decode('utf-8')

def verify_token(token):
    s = Serializer(app.config['SECRET_KEY'])
    try:
        return s.loads(token)['email']
    except SignatureExpired:
        abort(404)

@users.route('/sign_up', methods=['GET', 'POST'])
@um.user_denied
def sign_up():
    form = SignUpForm(request.form)
    if request.method == 'POST' and form.validate():
        hashed = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        db.users.insert_one({
            'name': form.name.data,
            'affiliation': form.affiliation.data,
            'email': form.email.data,
            'password': hashed,
            'created': datetime.utcnow(),
            'verified': False,
            'expires': datetime.utcnow() + timedelta(1)
        })
        token = get_token(form.email.data, expires=24*60*60)
        msg = Message(
            'Account Verification',
            sender=app.config['MAIL_USERNAME'],
            recipients=[form.email.data]
        )
        msg.body = f'''
Welcome to AcaDome! We are glad to have you onboard.
The last step in setting up your account is to verify your email address by clicking on the following link.

{url_for('users.verify', token=token, _external=True)}

If you have not signed up with us, please do not click on the above link.
The account associated with this email address will be deleted in 24 hours if not verified.

Yours sincerely,
Team AcaDome'''
        mail.send(msg)
        flash(f'An email has been sent to {form.email.data} with a link to verify your account. The link will be active for 24 hours, after which your account will be deleted if not verified. You cannot login until your account is verified.')
        return redirect(url_for('users.login'))
    return render_template('sign_up.html', title='Sign Up', um=um, form=form)

@users.route('/verify/<token>')
def verify(token):
    email = verify_token(token)
    db.users.update_one({'email': email}, {
        '$set': {'verified': True},
        '$unset': {'expires': ''}
    })
    if um.user:
        um.reset_user()
        um.set_user(db.users.find_one({'email': email}))
    flash('Thank you for verifying your account. You may proceed to login.')
    return redirect(url_for('users.login'))

@users.route('/login', methods=['GET', 'POST'])
@um.user_denied
def login():
    form = LoginForm(request.form)
    if request.method == 'POST' and form.validate():
        um.set_user(db.users.find_one({'email': form.email.data}))
        return redirect(url_for('users.account'))
    return render_template('login.html', title='Login', um=um, form=form)

@users.route('/')
@um.user_required
@um.admin_redirect
def account():
    articles = []
    for id in um.user['articles'][::-1]:
        articles.append(db.queue.find_one({'id': id}) or db.articles.find_one({'id': id}))
    return render_template('account.html', title='Account', articles=articles, um=um)

@users.route('/user_json')
@um.user_required
def user_json():
    return um.user

@users.route('/edit', methods=['GET', 'POST'])
@um.user_required
def edit_account():
    form = EditAccountForm(request.form)
    if request.method == 'POST' and form.validate():
        db.users.update_one({'email': um.user['email']}, {
            '$set': {
                'name': form.name.data,
                'affiliation': form.affiliation.data,
                'email': form.email.data
            }
        })
        if form.email.data != um.user['email']:
            db.users.update_one({'email': form.email.data}, {
                '$set': {
                    'verified': False,
                    'expires': datetime.utcnow() + timedelta(1)
                }
            })
            token = get_token(form.email.data, expires=24*60*60)
            msg = Message(
                'Account Verification',
                sender=app.config['MAIL_USERNAME'],
                recipients=[form.email.data]
            )
            msg.body = f'''
Your email address has been changed from {um.user['email']} to {form.email.data}. Please verify your new email address by clicking on the following link.

{url_for('users.verify', token=token, _external=True)}

If you have not made this change, please do not click on the above link.
The account associated with this email address will be deleted in 24 hours if not verified.

Yours sincerely,
Team AcaDome'''
            mail.send(msg)
            um.reset_user()
            flash(f'An email has been sent to {form.email.data} with a link to verify your account. The link will be active for 24 hours, after which your account will be deleted if not verified. You cannot login until your account is verified.')
            return redirect(url_for('users.login'))
        um.reset_user()
        um.set_user(db.users.find_one({'email': form.email.data}))
        return redirect(url_for('users.account'))
    return render_template('edit_account.html', title='Edit Account', um=um, form=form)

def reset_password(email):
    token = get_token(email)
    msg = Message(
        'Password Reset',
        sender=app.config['MAIL_USERNAME'],
        recipients=[email]
    )
    msg.body = f'''
To reset your password, click on the following link:

{url_for('users.reset_password2', token=token, _external=True)}

Yours sincerely,
Team AcaDome'''
    mail.send(msg)
    flash(f'An email has been sent to {email} with a link to reset your password. The link will expire in 5 minutes.')
    return redirect(url_for('users.logout'))

@users.route('/reset_password', methods=['GET', 'POST'])
def reset_password1():
    if um.user:
        return reset_password(um.user['email'])
    form = ResetPasswordForm1(request.form)
    if request.method == 'POST' and form.validate():
        return reset_password(form.email.data)
    return render_template('reset_password1.html', title='Reset password', um=um, form=form)

@users.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password2(token):
    email = verify_token(token)
    form = ResetPasswordForm2(request.form)
    if request.method == 'POST' and form.validate():
        hashed = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        db.users.update_one({'email': email}, {
            '$set': {'password': hashed}
        })
        flash('Your password has been updated. Please login again.')
        return redirect(url_for('users.logout'))
    return render_template('reset_password2.html', title='Reset password', um=um, form=form, token=token)

@users.route('/logout')
@um.user_required
def logout():
    um.reset_user()
    return redirect(url_for('users.login'))

@users.route('/delete', methods=['GET', 'POST'])
@um.user_required
def delete():
    form = DeleteForm(request.form)
    if request.method == 'POST' and form.validate():
        user = db.users.find_one({'email': um.user['email']})
        user['deleted'] = datetime.utcnow()
        db.deleted_users.insert_one(user)
        db.users.delete_one({'email': um.user['email']})
        msg = Message(
            'Account Deletion',
            sender=app.config['MAIL_USERNAME'],
            recipients=[um.user['email']]
        )
        msg.body = f'''
Your account has been deleted.

You can restore your account by emailing us at team.acadome@gmail.com.

Yours sincerely,
Team AcaDome'''
        mail.send(msg)
        um.reset_user()
        flash('Your account has been deleted. You can restore your account anytime by emailing us at team.acadome@gmail.com.')
        return redirect(url_for('articles.home'))
    return render_template('delete.html', title='Delete account', um=um, form=form)
