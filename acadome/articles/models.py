from acadome import db

class Article(db.Document):
    title = db.StringField()
    ref = db.StringField()
    authors = db.ListField(db.StringField())
    year = db.IntField()
    abstract = db.StringField()
    keywords = db.ListField(db.StringField())
    field = db.StringField()
    subfields = db.ListField(db.StringField())
    citations = db.ListField(db.StringField())
    doi = db.StringField()

    meta = {
        'collection': 'articles',
        'indexes': [
            {
                'fields': [
                    '$title',
                    '$authors',
                    '$abstract',
                    '$keywords',
                    '$field',
                    '$subfields'
                ],
                'default_language': 'english',
                'weights': {
                    'title': 8,
                    'authors': 6,
                    'abstract': 1,
                    'keywords': 10,
                    'field': 3,
                    'subfields': 5
                },
                'name': 'search'
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

class Field(db.Document):
    name = db.StringField()
    subs = db.ListField(db.StringField())

    meta = {
        'collection': 'fields'
    }
