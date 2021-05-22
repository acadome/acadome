from wtforms import Form, StringField, FileField, TextAreaField
from wtforms.validators import Length, Email, ValidationError, Regexp

def input_required(form, field):
    if len(field.data) == 0:
        raise ValidationError('')

class PublishForm(Form):
    name = StringField(label='Name *', validators=[Length(max=64), input_required, Regexp('^[a-zA-Z \-\']+$')])
    email = StringField(label='Email *', validators=[Email(), Length(max=254), input_required, Regexp('^[a-zA-Z0-9_\-\.]+@[a-zA-Z0-9\-\.]+\.[a-zA-Z]+$')])
    affiliation = StringField(label='Affiliation', validators=[Length(max=256), Regexp('^[a-zA-Z0-9 \,\.\-\']*$')])
    file = FileField(label='Upload')

class ContactForm(Form):
    name = StringField(label='Name *', validators=[Length(max=64), input_required, Regexp('^[a-zA-Z \-\']+$')])
    email = StringField(label='Email *', validators=[Email(), Length(max=254), input_required, Regexp('^[a-zA-Z0-9_\-\.]+@[a-zA-Z0-9\-\.]+\.[a-zA-Z]+$')])
    query = TextAreaField(label='Query *', validators=[Length(max=1024), input_required, Regexp('^[a-zA-Z0-9 \,\.\-\'\r\n]+$')])
