import os
import random
from datetime import datetime
from flask import render_template, redirect, url_for, request, flash, abort
from flask_mail import Message
from acadome import app, db, mail, um
from acadome.articles import articles
from acadome.articles.forms import PublishForm

@articles.route('/')
def home():
    query = request.args.get('search')
    if query:
        query = query.strip()
        articles = db.articles.find({'$text': {'$search': query}})
        return render_template('search.html', title=query, query=query, articles=articles, um=um)
    return render_template('home.html', um=um)

@articles.route('/fields')
def fields():
    fields = db.fields.find().sort([('name', 1)])
    return render_template('fields.html', title='Fields of research', fields=sorted(fields_), um=um)

@articles.route('/field/<string:field>')
def field_search(field):
    field = field.replace('_', ' ')
    if not db.fields.find_one({'field': field}):
        abort(404)
    articles = db.articles.find({'field': field}).sort([('year', -1), ('title', 1)])
    return render_template('search.html', title=field, articles=articles, um=um)

@articles.route('/author/<string:author>')
def author_search(author):
    author_ = author.replace('_', ' ')
    if not db.articles.count_documents({'authors': author_}):
        abort(404)
    articles = db.articles.find({'authors': author_}).sort([('year', -1), ('title', 1)])
    return render_template('search.html', title=author_, query=author_, articles=articles, um=um)

@articles.route('/article/<string:id>')
def article(id):
    article = db.articles.find_one({'id': id})
    return render_template('article.html', title=article['title'], article=article, um=um)

def generate_id():
    r = str(random.randint(10000000, 99999999))
    if db.queue.find_one({'id': r}) or db.articles.find_one({'id': r}):
        return generate_id()
    return r

@articles.route('/account/publish', methods=['GET', 'POST'])
@um.user_required
def publish():
    form = PublishForm(request.form)
    if request.method == 'POST' and form.validate():
        id = generate_id()
        if form.authors.data:
            authors = [ca.strip() for ca in form.authors.data.split(',')]
            authors.insert(0, um.user['name'])
        else:
            authors = [um.user['name']]
        keywords = [kw.strip() for kw in form.keywords.data.split(',')]
        reviewers = [rev.strip() for rev in form.reviewers.data.split(',')]
        db.queue.insert_one({
            'id': id,
            'title': form.title.data,
            'authors': authors,
            'submitted': datetime.utcnow(),
            'abstract': form.abstract.data,
            'keywords': keywords,
            'field': form.field.data,
            'reviewers': reviewers,
            'status': 'Submitted',
            'uploader': um.user['email']
        })
        db.users.update_one({'email': um.user['email']}, {
            '$push': {'articles': id}
        })
        file = request.files['file']
        msg1 = Message(
            'Preprint',
            sender=app.config['MAIL_USERNAME'],
            recipients=[app.config['MAIL_USERNAME']]
        )
        msg1.body = f'''
Uploaded by: {um.user['email']}'''
        filename = id
        path = app.root_path + url_for('articles.static', filename='pdfs/queue/' + filename)
        file.save(path)
        with app.open_resource(path, 'rb') as raw:
            msg1.attach(filename, file.mimetype, raw.read())
        mail.send(msg1)
        msg2 = Message(
            'Preprint received',
            sender=app.config['MAIL_USERNAME'],
            recipients=[um.user['email']]
        )
        msg2.body = '''
We have received your preprint. Thank you for choosing to publish with AcaDome.

Yours sincerely,
Team AcaDome'''
        mail.send(msg2)
        flash('Your preprint has been submitted successfully.')
        email = um.user['email']
        um.reset_user()
        um.set_user(db.users.find_one({'email': email}))
        return redirect(url_for('users.account'))
    return render_template('publish.html', title='Publish', um=um, form=form)
