from flask import render_template, request, flash
from flask_mail import Message
from acadome import app, um, mail
from acadome.gen import gen
from acadome.gen.forms import ContactForm

@gen.route('/about')
def about():
    return render_template('about.html', title='About', um=um)

@gen.route('/workflow')
def workflow():
    return render_template('workflow.html', title='Workflow', um=um)

@gen.route('/financial_model')
def finances():
    return render_template('finances.html', title='Financial model', um=um)

@gen.route('/user_agreement')
def user_agreement():
    return render_template('user_agreement.html', title='User agreement', um=um)

@gen.route('/publishing_agreement')
def publishing_agreement():
    return render_template('publishing_agreement.html', title='Publishing agreement', um=um)

@gen.route('/contact', methods=['GET', 'POST'])
def contact():
    form = ContactForm(request.form)
    if request.method == 'POST' and form.validate():
        msg1 = Message(
            'Query',
            sender=app.config['MAIL_USERNAME'],
            recipients=[app.config['MAIL_USERNAME']]
        )
        msg1.body = f'''
Name: {form.name.data}

Email: {form.email.data}

Query: {form.query.data}'''
        mail.send(msg1)
        msg2 = Message(
            'Query Received',
            sender=app.config['MAIL_USERNAME'],
            recipients=[form.email.data]
        )
        msg2.body = '''
We have received your query and will get back to you within two working days.
Thank you for your patience.

Yours sincerely,
Team AcaDome'''
        mail.send(msg2)
        flash('Your query has been submitted successfully.')
        return redirect(url_for('articles.home'))
    return render_template('contact.html', title='Contact', um=um, form=form)
