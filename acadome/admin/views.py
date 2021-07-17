from datetime import datetime
from flask import render_template, redirect, url_for, request, abort
from acadome import app, db, mail, um
from acadome.admin import admin
from acadome.admin.forms import EditArticleForm

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
    return render_template('admin_home.html', title='Admin', articles=articles, um=um)

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

@admin.route('/edit_article/<string:id>', methods=['GET', 'POST'])
@um.user_required
@um.access('admin')
def edit(id):
    article = find_article(id)
    form = EditArticleForm(request.form)
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
                'reviewers': reviewers,
                'edited': datetime.utcnow()
            }
        })
        return redirect(url_for('admin.article', id=id))
    return render_template('edit_article.html', title=f'Edit article | {id}', id=id, um=um, form=form)

@admin.route('/article/<string:id>/accept')
@um.user_required
@um.access('admin')
def accept(id):
    article = find_article(id)
    article['status'] = 'Accepted'
    article['accepted'] = datetime.utcnow()
    msg = Message(
        'Preprint Accepted',
        sender=app.config['MAIL_USERNAME'],
        recipients=[article['uploader']]
    )
    msg.body = '''
Your preprint has been accepted.

Yours sincerely,
Team AcaDome'''
    mail.send(msg)
    db.articles.insert_one(article)
    db.queue.delete_one({'id': id})
    return redirect(url_for('admin.home'))

@admin.route('/article/<string:id>/reject')
@um.user_required
@um.access('admin')
def reject(id):
    article = find_article(id)
    article['status'] = 'Rejected'
    article['rejected'] = datetime.utcnow()
    msg = Message(
        'Preprint Rejected',
        sender=app.config['MAIL_USERNAME'],
        recipients=[article['uploader']]
    )
    msg.body = '''
Your preprint has been rejected.

Yours sincerely,
Team AcaDome'''
    mail.send(msg)
    db.rejected.insert_one(article)
    db.queue.delete_one({'id': id})
    return redirect(url_for('admin.home'))
