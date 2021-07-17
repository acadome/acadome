from flask import render_template
from acadome import db, um
from acadome.editors import editors

@editors.route('/')
@um.user_required
@um.redirect('admin', 'admin.home')
@um.access('editor')
def home():
    articles = db.queue.find().sort([('submitted', 1)])
    return render_template('editors_home.html', title='Editor', articles=articles, um=um)

@editors.route('/article/<string:id>')
@um.user_required
@um.access('editor')
def article(id):
    article = db.queue.find_one({'id': id})
    return render_template('editors_article.html', title=article['title'], article=article, um=um)
