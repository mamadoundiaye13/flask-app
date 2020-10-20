from flask import Flask
from flask import render_template

app = Flask(__name__)

""" formulaire """
@app.route('/')
def index():
     return 'doit retourner le formulaire'

@app.route('/repos/')
def getAllRepos(name=None):
    return render_template('all-repos.html')

@app.route('/repos/<name>')
def getOneRepos(name=None):
    return render_template('one-repos.html', name=name)
