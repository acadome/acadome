from wtforms import Form, StringField, FileField
from wtforms.validators import Length, Email, ValidationError

def input_required(form, field):
    if len(field.data) == 0:
        raise ValidationError('This field is required.')

class PublishForm(Form):
    name = StringField(label='Name *', validators=[Length(max=64), input_required])
    email = StringField(label='Email *', validators=[Email(), Length(max=64), input_required])
    inst = StringField(label='Research institute', validators=[Length(max=128)])
    file = FileField(label='Upload')
