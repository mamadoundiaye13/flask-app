from flask import Flask, redirect
from flask import render_template
import requests
from config import Config
from form import IndexForm

app = Flask(__name__)
app.config.from_object(Config)

""" formulaire """
@app.route('/', methods=['POST', 'GET'])
def index():
    form = IndexForm()
    if form.validate_on_submit():
        return redirect('http://127.0.0.1:5000/user/' + form.username.data)

    return render_template('index.html', title='Username', form=form)

@app.route('/user/repos/<name>')
def getAllRepos(name=None):
    url = "https://api.github.com/users/" + name  + "/repos"
    r = requests.get(url)
    json_obj = r.json()

    repos = list(json_obj)

    return render_template('all-repos.html', repos = repos)

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

if __name__ == '__main__' :
    app.run(debug = True)
