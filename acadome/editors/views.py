from flask import render_template, redirect, url_for, abort
from acadome import db, um
from acadome.editors import editors

def find_article(id):
    article = db.queue.find_one({'id': id})
    if not article:
        abort(404)
    return article

@editors.route('/')
@um.user_required
@um.redirect('admin', 'admin.home')
@um.access('editor')
def home():
    articles = db.queue.find().sort([('submitted', 1)])
    fields = db.fields.find().sort([('name', 1)])
    return render_template('editors_home.html', title='Editor', articles=articles, fields=fields, um=um)

@editors.route('/article/<string:id>')
@um.user_required
@um.access('editor')
def article(id):
    article = find_article(id)
    return render_template('editors_article.html', title=article['title'], article=article, um=um)

@editors.route('/article/<string:id>/accept')
@um.user_required
@um.access('editor')
def accept_article(id):
    article = find_article(id)
    db.queue.update_one({'id': id}, {
        '$push': {'votes.accept': um.user['name']}
    })
    return redirect(url_for('editors.article', id=id))

@editors.route('/article/<string:id>/reject')
@um.user_required
@um.access('editor')
def reject_article(id):
    article = find_article(id)
    db.queue.update_one({'id': id}, {
        '$push': {'votes.reject': um.user['name']}
    })
    return redirect(url_for('editors.article', id=id))
