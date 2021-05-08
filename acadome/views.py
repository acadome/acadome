import os
from flask import render_template, redirect, request, url_for
from werkzeug.utils import secure_filename
from flask_mail import Message
from . import app, db, mail
from .forms import PublishForm

@app.route('/')
def home():
    query = request.args.get('search')
    if query:
        # query database, pagination
        return render_template('search.html', title=query, query=query)
    return render_template('home.html')

@app.route('/about')
def about():
    return render_template('about.html', title='About')

@app.route('/publish', methods=['GET', 'POST'])
def publish():
    form = PublishForm(request.form)
    if request.method == 'POST' and form.validate():
        file = request.files['file']
        if not file.filename:
            return redirect(url_for('publish'))

        msg1 = Message(form.name.data.strip(), sender='editor.acadome@gmail.com', recipients=['editor.acadome@gmail.com'])
        if form.inst.data:
            msg1.body = f'''Email: {form.email.data}
Research institute: {form.inst.data}'''
        else:
            msg1.body = f'Email: {form.email.data}'
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.root_path + '/temp', filename))
        with app.open_resource('temp/' + filename, 'rb') as raw:
            msg1.attach('temp/' + filename, file.mimetype, raw.read())
        mail.send(msg1)
        os.remove(os.path.join(app.root_path + '/temp', filename))

        msg2 = Message('Research manuscript received', sender='editor.acadome@gmail.com', recipients=[form.email.data])
        msg2.body = '''This is to confirm that we have received your research manuscript. You can expect a response within three working days.

Thank you for choosing to publish with AcaDome.

Yours sincerely,
The Editorial Team'''
        mail.send(msg2)

        return redirect(url_for('home'))
    return render_template('publish.html', title='Publish', form=form)

@app.route('/contact')
def contact():
    return render_template('contact.html', title='Contact')

@app.route('/fields')
def fields():
    # sort fields
    return render_template('fields.html', title='Fields of research')

@app.route('/profile/<string:author>')
def profile(author):
    arr = author.split('_')
    for x in range(len(arr)):
        arr[x] = f'{arr[x][0].upper()}{arr[x][1:]}'
    name = ' '.join(arr)
    # find all articles published by author (similar to search)
    return render_template('profile.html', title=name, author=name)
