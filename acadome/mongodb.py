def sort_subfields():
    for field in Field.objects:
        field.subs = sorted(field.subs)
        field.save()

def _random_ref():
    import random
    r = str(random.randint(10000000000, 99999999999))
    for article in Article.objects:
        if r == article.ref:
            return random_ref()
    return r

def add_article():
    Article(
        ref=_random_ref(),
        title='',
        authors=[''],
        year=,
        abstract='',
        keywords='',
        field='',
        subfields=[''],
        doi='',
        citations=['']
    ).save()

def add_author():
    Author(
        name='',
        email='',
        affil=''
    ).save()

def add_field():
    Field(
        name='',
        subs=['']
    ).save()

def modify_doc():
    article = Article.objects
    author = Author.objects
    field = Field.objects
