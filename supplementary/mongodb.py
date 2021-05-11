import mongoengine as me

me.connect(host='')

class Article(me.Document):
    title = me.StringField()
    authors = me.ListField(me.StringField())
    year = me.IntField()
    abstract = me.StringField()
    keywords = me.ListField(me.StringField())
    field = me.StringField()
    subfields = me.ListField(me.StringField())
    citations = me.IntField()
    doi = me.StringField()

    meta = {
        'collection': 'articles',
    }

class Author(me.Document):
    name = me.StringField()
    email = me.EmailField()
    affil = me.StringField()

    meta = {
        'collection': 'authors'
    }

class Field(me.Document):
    name = me.StringField()
    subs = me.ListField(me.StringField())

    meta = {
        'collection': 'fields'
    }
