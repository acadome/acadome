from flask import render_template, request, abort
from pymongo import ASCENDING, DESCENDING
from acadome import db, um
from acadome.articles import articles

@articles.route('/')
def home():
    query = request.args.get('search')
    if query:
        query = query.strip()
        articles = db.articles.find({'$text': {'$search': query}})
        return render_template(
            'search.html',
            title=query,
            query=query,
            articles=articles,
            um=um
        )
    return render_template(
        'home.html',
        um=um
    )

@articles.route('/fields_of_research')
def fields():
    fields_ = db.fields.find().sort('name')
    return render_template(
        'fields.html',
        title='Fields of research',
        fields=fields_,
        um=um
    )

@articles.route('/field/<string:field>')
def subfields(field):
    field_ = field[0].upper() + field.replace('_', ' ')[1:]
    field = db.fields.find_one({'name': field_})
    if not field:
        abort(404)
    return render_template(
        'fields.html',
        title=field_,
        field=field,
        um=um
    )

@articles.route('/subfield/<string:subfield>')
def subfield_search(subfield):
    subfield_ = subfield.replace('_', ' ')
    if not db.fields.find_one({'subs': subfield_}):
        abort(404)
    articles = db.articles.find({'subfields': subfield_}).sort([('year', DESCENDING), ('title', ASCENDING)])
    return render_template(
        'search.html',
        title=subfield_,
        query=subfield_,
        articles=articles,
        um=um
    )

@articles.route('/author/<string:author>')
def author_search(author):
    author_ = author.replace('_', ' ')
    if not db.authors.find_one({'name': author_}):
        abort(404)
    articles = db.articles.find({'authors': author_}).sort([('year', DESCENDING), ('title', ASCENDING)])
    return render_template(
        'search.html',
        title=author_,
        query=author_,
        articles=articles,
        um=um
    )

@articles.route('/article/<string:ref>')
def article(ref):
    article = db.articles.find_one({'ref': ref})
    return render_template(
        'article.html',
        title=article['title'],
        article=article,
        um=um
    )
