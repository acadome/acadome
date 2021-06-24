from wtforms import Form, StringField, FileField, TextAreaField, BooleanField
from wtforms.validators import Length, ValidationError, Regexp

def required(form, field):
    if len(field.data) == 0:
        raise ValidationError('')

def checkbox(form, field):
    if not field.data:
        raise ValidationError('')

class PublishForm(Form):
    name = StringField(
        label='Name *',
        validators=[
            required,
            Length(max=64),
            Regexp(
                '^[a-zA-Z \-\']+$',
                message='Invalid characters in name.'
            )
        ]
    )
    email = StringField(
        label='Email *',
        validators=[
            required,
            Length(max=254),
            Regexp(
                '^[a-zA-Z0-9_\-\.]+@[a-zA-Z0-9\-\.]+$',
                message='Invalid email address.'
            )
        ]
    )
    affiliation = StringField(
        label='Affiliation',
        validators=[
            Length(max=256),
            Regexp(
                '^[a-zA-Z0-9 \,\.\-\']*$',
                message='Invalid characters in affiliation.'
            )
        ]
    )
    file = FileField(
        label='Upload'
    )
    agreement = BooleanField(
        validators=[
            checkbox
        ]
    )

class ContactForm(Form):
    name = StringField(
        label='Name *',
        validators=[
            required,
            Length(max=64),
            Regexp(
                '^[a-zA-Z \-\']+$',
                message='Invalid characters in name.'
            )
        ]
    )
    email = StringField(
        label='Email *',
        validators=[
            required,
            Length(max=254),
            Regexp(
                '^[a-zA-Z0-9_\-\.]+@[a-zA-Z0-9\-\.]+$',
                message='Invalid email address.'
            )
        ]
    )
    query = TextAreaField(
        label='Query *',
        validators=[
            required,
            Length(max=1024),
            Regexp(
                '^[a-zA-Z0-9 \,\.\-\'\r\n]+$',
                message='Invalid characters in query.'
            )
        ]
    )
