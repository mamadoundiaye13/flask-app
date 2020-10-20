from flask import Flask, redirect
from flask import render_template
import requests
from config import Config
from form import IndexForm

app = Flask(__name__)
app.config.from_object(Config)
app.debug = True

""" formulaire """
@app.route('/', methods=['POST', 'GET'])
def index():
    form = IndexForm()
    if form.validate_on_submit():
        return redirect('http://127.0.0.1:5000/user/' + form.username.data)

    return render_template('index.html', title='Username', form=form)

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
    response = requests.get(url)
    user = response.json()

    if response.status_code == 200:
        return render_template('user.html', user = user)
    elif response.status_code == 404:
        return "Not Found"

@app.route('/repos/<name>')
def getOneRepos(name=None):
    return render_template('one-repos.html', name=name)
