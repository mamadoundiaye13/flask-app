from flask import Flask
from flask import render_template
import requests
app = Flask(__name__)

""" formulaire """
@app.route('/')
def index():
     return render_template('index.html')

@app.route('/repos/')
def getAllRepos():
    url = "https://api.github.com/users/alex/repos"
    r = requests.get(url)
    json_obj = r.json()

    owner = list(json_obj["owner"])

    return render_template('all-repos.html', owner = owner)

@app.route('/user/<name>')
@app.route('/user/')
def getUser(name=None):
    url = "https://api.github.com/users/"+ name
    r = requests.get(url)
    user = r.json()

    return render_template('user.html', user = user)

@app.route('/repos/<name>')
def getOneRepos(name=None):
    return render_template('one-repos.html', name=name)
