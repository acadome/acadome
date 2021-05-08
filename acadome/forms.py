from wtforms import Form, StringField, FileField
from wtforms.validators import InputRequired, Length, Email, ValidationError

def input_required(form, field):
    if len(field.data) == 0:
        raise ValidationError('This field is required.')

class PublishForm(Form):
    fname = StringField(label='First name *', validators=[Length(max=20), input_required])
    lname = StringField(label='Last name *', validators=[Length(max=20), input_required])
    email = StringField(label='Email *', validators=[Email(), Length(max=40), input_required])
    inst = StringField(label='Research institute', validators=[Length(max=60)])
    file = FileField(label='Upload PDF file *')
