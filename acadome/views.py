from flask import render_template
from . import app, db

@app.route('/')
def homepage():
    # handle searching
    return render_template('home.html')

@app.route('/about')
def about():
    return render_template('about.html', title='About')

@app.route('/publish')
def publish():
    # publishing form
    return render_template('publish.html', title='Publish')

@app.route('/profile/<string:author>')
def profile(author):
    arr = author.split('_')
    for x in range(len(arr)):
        arr[x] = f'{arr[x][0].upper()}{arr[x][1:]}'
    name = ' '.join(arr)
    # find all articles published by author
    return render_template('profile.html', title=name, author=name)
