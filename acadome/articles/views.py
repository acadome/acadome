from flask import render_template, request
from acadome import db
from acadome.articles import articles
from acadome.articles.models import Article, Author, Field

def count_citations(set):
    for src in set:
        src.count = 0
        for article in Article.objects:
            if src.ref in article.citations:
                src.count += 1

@articles.route('/')
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

@articles.route('/fields_of_research')
def fields():
    fields_ = Field.objects().order_by('name')
    return render_template(
        'fields.html',
        title='Fields of research',
        fields=fields_
    )

@articles.route('/field/<string:field>')
def subfields(field):
    field = field[0].upper() + field.replace('_', ' ')[1:]
    field_ = Field.objects.get_or_404(name=field)
    return render_template(
        'fields.html',
        title=field,
        field=field_
    )

@articles.route('/subfield/<string:subfield>')
def subfield_search(subfield):
    subfield_ = subfield.replace('_', ' ')
    Field.objects.get_or_404(subs__iexact=subfield_)
    page = request.args.get('page', 1, type=int)
    articles = Article.objects(subfields__iexact=subfield_).order_by('-year', 'title').paginate(page=page, per_page=20)
    count_citations(articles.items)
    return render_template(
        'search.html',
        title=subfield_,
        query=subfield_,
        articles=articles,
        subfield=subfield_
    )

@articles.route('/author/<string:author>')
def author_search(author):
    author_ = author.replace('_', ' ')
    Author.objects.get_or_404(name__iexact=author_)
    page = request.args.get('page', 1, type=int)
    articles = Article.objects(authors__iexact=author_).paginate(page=page, per_page=20)
    count_citations(articles.items)
    return render_template(
        'search.html',
        title=author_,
        query=author_,
        articles=articles,
        author=author_
    )

@articles.route('/article/<string:ref>')
def article(ref):
    article = Article.objects.get_or_404(ref=ref)
    count_citations([article])
    return render_template(
        'article.html',
        title=article.title,
        article=article
    )
