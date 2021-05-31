from flask import render_template, redirect, request, url_for, abort, flash
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

@app.route('/')
def home():
    page = request.args.get('page', 1, type=int)
    query = request.args.get('search')
    if query:
        query = query.strip()
        articles = Article.objects.search_text(query).order_by('$text_score', '-year', 'title').paginate(page=page, per_page=20)
        count_citations(articles.items)
        return render_template(
            'search.html',
            title=query,
            query=query,
            articles=articles
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
        _, ext = os.path.splitext(file.filename)
        if ext.lower() != '.pdf':
            return redirect(url_for('publish'))
        msg1 = Message(form.name.data.strip(), sender='team.acadome@gmail.com', recipients=['team.acadome@gmail.com'])
        if form.affiliation.data:
            msg1.body = f'''Email: {form.email.data}

Affiliation: {form.affiliation.data}'''
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
        flash('Submitted successfully.')
        return redirect(url_for('publish'))
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
        flash('Submitted successfully.')
        return redirect(url_for('contact'))
    return render_template(
        'contact.html',
        title='Contact',
        form=form
    )

@app.route('/fields_of_research')
def fields():
    fields_ = Field.objects().order_by('name')
    return render_template(
        'fields.html',
        title='Fields of research',
        fields=fields_
    )

@app.route('/field/<string:field>')
def subfields(field):
    field = field[0].upper() + field.replace('_', ' ')[1:]
    field_ = Field.objects.get_or_404(name=field)
    return render_template(
        'fields.html',
        title=field,
        field=field_
    )

@app.route('/subfield/<string:subfield>')
def subfield_search(subfield):
    subfield_ = subfield[0].upper() + subfield[1:].lower().replace('_', ' ')
    Field.objects.get_or_404(subs__contains=subfield_)
    page = request.args.get('page', 1, type=int)
    articles = Article.objects(subfields__contains=subfield_).order_by('-year', 'title').paginate(page=page, per_page=20)
    count_citations(articles.items)
    return render_template(
        'search.html',
        title=subfield_,
        query=subfield_,
        articles=articles
    )

@app.route('/author/<string:author>')
def author_search(author):
    arr = [a[0].upper() + a[1:].lower() for a in author.split('_')]
    author_ = ' '.join(arr)
    Author.objects.get_or_404(name=author_)
    page = request.args.get('page', 1, type=int)
    articles = Article.objects(authors__contains=author_).paginate(page=page, per_page=20)
    count_citations(articles.items)
    return render_template(
        'search.html',
        title=author_,
        query=author_,
        articles=articles
    )

@app.route('/article/<string:ref>')
def article(ref):
    article = Article.objects.get_or_404(ref=ref)
    count_citations([article])
    return render_template(
        'article.html',
        title=article.title,
        article=article
    )

@app.route('/publishing_agreement')
def agreement():
    return render_template(
        'agreement.html',
        title='Publishing agreement'
    )

@app.route('/financial_model')
def finances():
    return render_template(
        'finances.html',
        title='Financial model'
    )

@app.route('/arc')
def arc():
    return render_template(
        'arc.html',
        title='AcaDome Reseach Council'
    )

@app.route('/mongodb')
def mongodb():
    abort(404)
