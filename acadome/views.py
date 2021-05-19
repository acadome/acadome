from flask import render_template, redirect, request, url_for, abort
from werkzeug.utils import secure_filename
from flask_mail import Message
from acadome import app, db, mail
from acadome.models import Article, Author, Field
from acadome.forms import PublishForm, ContactForm
import os

def count_citations(set):
    for src in set:
        src.count = 0
        for article in Article.objects:
            if src.ref in article.citations:
                src.count += 1

def split_columns(set):
    col1, col2 = [], []
    for i in range(len(set)):
        if i%2:
            col2.append(set[i])
        else:
            col1.append(set[i])
    return col1, col2

@app.route('/')
def home():
    page = request.args.get('page', 1, type=int)
    query = request.args.get('search')
    if query:
        fields = Field.objects
        norm = query[0].upper() + query[1:]
        for field in fields:
            if norm in field.subs:
                return redirect(url_for('subfields', subfield=norm.lower().replace(' ', '_')))
        articles = Article.objects.search_text(query).order_by('$text_score', '-year', 'title').paginate(page=page, per_page=20)
        count_citations(articles.items)
        col1, col2 = split_columns(articles.items)
        return render_template(
            'search.html',
            title=query,
            query=query,
            articles=articles,
            column1=col1,
            column2=col2
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

Affiliation: {form.affil.data}'''
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

@app.route('/subfield/<string:subfield>')
def subfields(subfield):
    subfield = subfield[0].upper() + subfield[1:].replace('_', ' ')
    if not Field.objects(subs__contains=subfield).first():
        abort(404)
    query = request.args.get('search')
    if query:
        return redirect(url_for('home', search=query))
    page = request.args.get('page', 1, type=int)
    articles = Article.objects(subfields__contains=subfield).order_by('-year', 'title').paginate(page=page, per_page=20)
    count_citations(articles.items)
    col1, col2 = split_columns(articles.items)
    return render_template(
        'search.html',
        title=subfield,
        query=subfield.lower(),
        articles=articles,
        column1=col1,
        column2=col2
    )

@app.route('/profile/<string:author>')
def profile(author):
    arr = author.split('_')
    for a in range(len(arr)):
        arr[a] = arr[a][0].upper() + arr[a][1:]
    name = ' '.join(arr)
    author = Author.objects(name=name).first()
    if not author:
        abort(404)
    page = request.args.get('page', 1, type=int)
    articles = Article.objects(authors__contains=name).paginate(page=page, per_page=20)
    count_citations(articles.items)
    col1, col2 = split_columns(articles.items)
    return render_template(
        'profile.html',
        title=name,
        author_=author,
        articles=articles,
        column1=col1,
        column2=col2
    )

@app.route('/mongodb')
def mongodb():
    abort(404)
