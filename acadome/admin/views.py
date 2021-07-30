from datetime import datetime
from flask import render_template, redirect, url_for, request, abort
from acadome import app, db, mail, um
from acadome.admin import admin
from acadome.forms.models import EditArticleForm

def find_article(id):
    article = db.queue.find_one({'id': id})
    if not article:
        abort(404)
    return article

@admin.route('/')
@um.user_required
@um.access('admin')
def home():
    articles = db.queue.find().sort([('submitted', 1)])
    fields = db.fields.find().sort([('name', 1)])
    return render_template('admin_home.html', title='Admin', articles=articles, fields=fields, um=um)

@admin.route('/article/<string:id>')
@um.user_required
@um.access('admin')
def article(id):
    article = find_article(id)
    return render_template('admin_article.html', title=article['title'], article=article, um=um)

@admin.route('/article_json/<string:id>')
@um.user_required
@um.access('admin')
def article_json(id):
    article = find_article(id)
    article.pop('_id', None)
    return article

@admin.route('/article/<string:id>/edit', methods=['GET', 'POST'])
@um.user_required
@um.access('admin')
def edit(id):
    article = find_article(id)
    form = EditArticleForm(data=request.get_json()) if request.get_json() else EditArticleForm(request.form)
    if request.method == 'POST' and form.validate():
        authors = [au.strip() for au in form.authors.data.split(',')]
        keywords = [kw.strip() for kw in form.keywords.data.split(',')]
        reviewers = [rev.strip() for rev in form.reviewers.data.split(',')]
        db.queue.update_one({'id': id}, {
            '$set': {
                'title': form.title.data,
                'authors': authors,
                'abstract': form.abstract.data,
                'keywords': keywords,
                'field': form.field.data,
                'reviewers': reviewers
            }
        })
        return url_for('admin.article', id=id) if request.get_json() else redirect(url_for('admin.article'))
    return render_template('edit_article.html', title='Edit article', id=id, um=um, form=form)

@admin.route('/article/<string:id>/update_status', methods=['GET', 'POST'])
@um.user_required
@um.access('admin')
def update_status(id):
    article = find_article(id)
    if request.method == 'POST':
        db.queue.update_one({'id': id}, {
            '$set': {'status': request.form.get('status')}
        })
        if request.form.get('status') == 'Accepted':
            db.queue.update_one({'id': id}, {
                '$set': {
                    'accepted': datetime.utcnow(),
                    'preprint': True,
                    'editor': request.form.get('editor')
                }
            })
            msg = Message(
                'Preprint Accepted',
                sender=app.config['MAIL_USERNAME'],
                recipients=[article['uploader']]
            )
            msg.body = '''
Your preprint has been accepted by our editorial board.

Yours sincerely,
Team AcaDome'''
            mail.send(msg)
            db.articles.insert_one(db.queue.find_one({'id': id}))
        elif request.form.get('status') == 'Rejected':
            db.queue.update_one({'id': id}, {
                '$set': {'rejected': datetime.utcnow()}
            })
            db.rejected.insert_one(db.queue.find_one({'id': id}))
            db.queue.delete_one({'id': id})
            msg = Message(
                sender=app.config['MAIL_USERNAME'],
                recipients=[article['uploader']]
            )
            msg.body = '''
Your preprint has been rejected by our editorial board.

Yours sincerely,
Team AcaDome'''
            mail.send(msg)
        elif request.form.get('status') == 'Being typeset':
            db.typeset.insert_one({'id': id})
        elif request.form.get('status') == 'Published':
            db.queue.update_one({'id': id}, {
                '$set': {
                    'published': datetime.utcnow(),
                    'preprint': False
                }
            })
            db.articles.delete_one({'id': id})
            db.articles.insert_one(db.queue.find_one({'id': id}))
            db.queue.delete_one({'id': id})
            return redirect(url_for('admin.home'))
        return redirect(url_for('admin.article', id=id))
    editors = db.users.find({'role': 'editor'})
    return render_template('update_status.html', title='Update status', article=article, editors=editors, um=um)
