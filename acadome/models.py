from acadome import db

class Article(db.Document):
    title = db.StringField()
    authors = db.ListField(db.StringField())
    year = db.IntField()
    field = db.StringField()
    subfields = db.ListField(db.StringField())
    abstract = db.StringField()
    keywords = db.ListField(db.StringField())
    citations = db.IntField()

    meta = {
        'collection': 'articles',
        'indexes': [
            {
                'fields': [
                    '$title',
                    '$authors',
                    '$keywords',
                    '$field'
                ],
                'default_language': 'english',
                'weights': {
                    'title': 4,
                    'authors': 8,
                    'keywords': 2,
                    'field': 1
                },
                'name': 'demo'
            }
        ]
    }

class Author(db.Document):
    name = db.StringField()
    email = db.EmailField()
    affil = db.StringField()

    meta = {
        'collection': 'authors'
    }
