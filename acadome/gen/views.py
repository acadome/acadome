from flask import render_template, redirect, request, url_for, abort, flash
from werkzeug.utils import secure_filename
from flask_mail import Message
from acadome import app, db, mail
from acadome.gen import gen
from acadome.gen.forms import PublishForm, ContactForm
import os

@gen.route('/about')
def about():
    return render_template(
        'about.html',
        title='About'
    )

@gen.route('/arc')
def arc():
    return render_template(
        'arc.html',
        title='AcaDome Reseach Council'
    )

@gen.route('/financial_model')
def finances():
    return render_template(
        'finances.html',
        title='Financial model'
    )

@gen.route('/publish', methods=['GET', 'POST'])
def publish():
    form = PublishForm(request.form)
    if request.method == 'POST' and form.validate():
        file = request.files['file']
        _, ext = os.path.splitext(file.filename)
        if ext.lower() != '.pdf':
            return redirect(url_for('gen.publish'))
        msg1 = Message(form.name.data.strip(), sender='team.acadome@gmail.com', recipients=['team.acadome@gmail.com'])
        if form.affiliation.data:
            msg1.body = f'''Email: {form.email.data}

Affiliation: {form.affiliation.data}'''
        else:
            msg1.body = f'Email: {form.email.data}'
        filename = secure_filename(file.filename)
        path = app.root_path + url_for('gen.static', filename='pdfs/temp/' + filename)
        file.save(path)
        with app.open_resource(path, 'rb') as raw:
            msg1.attach(filename, file.mimetype, raw.read())
        mail.send(msg1)
        os.remove(path)
        msg2 = Message('Research manuscript received', sender='team.acadome@gmail.com', recipients=[form.email.data])
        msg2.body = '''This is to confirm that we have received your research manuscript and will get back to you within three working days.

Thank you for choosing to publish with AcaDome.

Yours sincerely,
AcaDome'''
        mail.send(msg2)
        flash('Submitted successfully.')
        return redirect(url_for('gen.publish'))
    return render_template(
        'publish.html',
        title='Publish',
        form=form
    )

@gen.route('/publishing_agreement')
def agreement():
    return render_template(
        'agreement.html',
        title='Publishing agreement'
    )

@gen.route('/contact', methods=['GET', 'POST'])
def contact():
    form = ContactForm(request.form)
    if request.method == 'POST' and form.validate():
        msg1 = Message(form.name.data.strip(), sender='team.acadome@gmail.com', recipients=['team.acadome@gmail.com'])
        msg1.body = f'''Email: {form.email.data}

Query: {form.query.data}'''
        mail.send(msg1)
        msg2 = Message('Query received', sender='team.acadome@gmail.com', recipients=[form.email.data])
        msg2.body = '''This is to confirm that we have received your query and will get back to you within three working days.

Yours sincerely,
AcaDome'''
        mail.send(msg2)
        flash('Submitted successfully.')
        return redirect(url_for('gen.contact'))
    return render_template(
        'contact.html',
        title='Contact',
        form=form
    )

@gen.route('/mongodb')
def mongodb():
    abort(404)
