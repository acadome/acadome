from flask import render_template, redirect, request, url_for, abort
from werkzeug.utils import secure_filename
from flask_mail import Message
from acadome import app, db, mail
from acadome.models import Article, Author, Field
from acadome.forms import PublishForm, ContactForm
import os

@app.route('/')
def home():
    page = request.args.get('page', 1, type=int)
    query = request.args.get('search')
    if query:
        articles = Article.objects.search_text(query).order_by('$text_score', '-year', 'title').paginate(page=page, per_page=20)
        fields = Field.objects.order_by('name')
        column1, column2 = [], []
        for i in range(len(articles.items)):
            if i%2:
                column2.append(articles.items[i])
            else:
                column1.append(articles.items[i])
        return render_template(
            'search.html',
            title=query,
            query=query,
            articles=articles,
            column1=column1,
            column2=column2,
            fields=fields
        )
    return render_template('home.html')

@app.route('/about')
def about():
    return render_template(
        'about.html',
        title='About'
    )

@app.route('/publish', methods=['GET', 'POST'])
def publish():
    form = PublishForm(request.form)
    if request.method == 'POST' and form.validate():
        file = request.files['file']
        if file.filename[-4:] != '.pdf':
            return redirect(url_for('publish'))
        msg1 = Message(form.name.data.strip(), sender='team.acadome@gmail.com', recipients=['team.acadome@gmail.com'])
        if form.affil.data:
            msg1.body = f'''Email: {form.email.data}

Research institute: {form.affil.data}'''
        else:
            msg1.body = f'Email: {form.email.data}'
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.root_path + '/temp', filename))
        with app.open_resource('temp/' + filename, 'rb') as raw:
            msg1.attach(filename, file.mimetype, raw.read())
        mail.send(msg1)
        os.remove(os.path.join(app.root_path + '/temp', filename))
        msg2 = Message('Research manuscript received', sender='team.acadome@gmail.com', recipients=[form.email.data])
        msg2.body = '''This is to confirm that we have received your research manuscript and will get back to you within three working days.

Thank you for choosing to publish with AcaDome.

Yours sincerely,
Team AcaDome'''
        mail.send(msg2)
        return redirect(url_for('home'))
    return render_template(
        'publish.html',
        title='Publish',
        form=form
    )

@app.route('/contact', methods=['GET', 'POST'])
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
Team AcaDome'''
        mail.send(msg2)
        return redirect(url_for('home'))
    return render_template(
        'contact.html',
        title='Contact',
        form=form
    )

@app.route('/fields-of-research')
def fields():
    fields_ = Field.objects().order_by('name')
    return render_template(
        'fields.html',
        title='Fields of research',
        fields=fields_
    )

@app.route('/profile/<string:author>')
def profile(author):
    arr = author.split('_')
    for a in range(len(arr)):
        arr[a] = arr[a][0].upper() + arr[a][1:]
    name = ' '.join(arr)
    page = request.args.get('page', 1, type=int)
    author = Author.objects(name=name).first()
    if not author:
        abort(404)
    articles = Article.objects(authors__contains=name).paginate(page=page, per_page=20)
    column1, column2 = [], []
    for i in range(len(articles.items)):
        if i%2:
            column2.append(articles.items[i])
        else:
            column1.append(articles.items[i])
    return render_template(
        'profile.html',
        title=name,
        author_=author,
        articles=articles,
        column1=column1,
        column2=column2
    )
