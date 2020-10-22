from flask import render_template, url_for, Flask, redirect, request
import requests
from config import *
from form import IndexForm
from bs4 import BeautifulSoup as bs
from flask_mysqldb import MySQL
import pandas as pd
import matplotlib.pyplot as plt
import os
import time
import numpy as np

app = Flask(__name__, static_folder='assets')
app.config.from_object(Config)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'root'
app.config['MYSQL_DB'] = 'DatabaseFlask'

mysql = MySQL(app)

@app.route('/', methods=['POST', 'GET'])
def index():
    form = IndexForm()
    cur = mysql.connection.cursor()
    if form.validate_on_submit() and request.method == "POST":
        # Insertion du login tapé dans le input
        try:
            cur.execute("INSERT INTO user (username, date) VALUES (%s, current_timestamp())", (form.username.data,))
            mysql.connection.commit()
            return redirect(url_for('getUser', name=form.username.data))
        except Exception as e:
            print(e)
            return redirect(url_for('getUser', name=form.username.data))

    # Recupération des users cherchés
    try:
        query = "SELECT * from user"
        cur.execute(query)
        history = cur.fetchall()
        return render_template('index.html',
            form=form,
            history = list(history)
            )

    except Exception as e:
        return (str(e))

@app.route('/user/<name>')
@app.route('/user/')
def getUser(name=None):
    url = "https://api.github.com/users/"+ name
    response = requests.get(url)
    user = response.json()

    urlRepo = "https://api.github.com/users/" + name  + "/repos"
    responseRepo = requests.get(urlRepo)
    json_obj_repos = responseRepo.json()
    repos = list(json_obj_repos)

    urlEvents = "https://api.github.com/users/" + name  + "/received_events"
    responseEvents = requests.get(urlEvents)
    json_obj_events = responseEvents.json()
    reposEvents = list(json_obj_events)

    urlFollowers = "https://api.github.com/users/" + name  + "/followers"
    responseFollowers = requests.get(urlFollowers)
    json_obj_followers = responseFollowers.json()
    reposFollowers = list(json_obj_followers)

    urlFollowings = "https://api.github.com/users/" + name  + "/following"
    responseFollowings = requests.get(urlFollowings)
    json_obj_followings = responseFollowings.json()
    reposFollowings = list(json_obj_followings)

    urlAvatar = "https://avatars3.githubusercontent.com/u/" + "23127854" + "?v=4"

    if response.status_code == 200:
        return render_template('user.html',
            user = user,
            urlAvatar = urlAvatar,
            repos = repos,
            reposEvents = reposEvents,
            reposFollowers = reposFollowers,
            reposFollowings = reposFollowings
            )

    else:
        return render_template('error.html',
            status_code = response.status_code,
            limit = int(response.headers['X-RateLimit-Remaining']),
            response = response.json()
            )

@app.route('/repos/<name>/<id>/<reposName>')
@app.route('/repos/<name>')
@app.route('/repos/')
def getOneRepos(name=None, id=None, reposName = None):

    urlRepo = "https://api.github.com/users/" + name  + "/repos"
    responseRepo = requests.get(urlRepo)
    json_obj_repos = responseRepo.json()
    repos = list(json_obj_repos)

    urlLanguages = "https://api.github.com/repos/"+name+"/"+reposName+"/languages"
    responseLanguages = requests.get(urlLanguages)
    json_obj_languages = responseLanguages.json()
    languages = list(json_obj_languages)

    return render_template('one-repos.html',
        repos = repos,
        id = int(id),
        languages = languages
        )

@app.route('/infos/')
def infos():
    url ="https://sebastien.saunier.me/blog/2014/05/13/classement-technologique-des-villes-francaises.html"
    url2 = "https://www.journaldunet.com/solutions/dsi/1420928-quels-sont-les-langages-les-mieux-maitrises-par-les-dev-francais/"

    r = requests.get(url2)
    page2 = r.content
    page = requests.get(url)

    s = bs(page2, 'html.parser')
    images = s.find_all('img')
    imgs = []

    for img in images:
        if (img.has_attr('src') and img['src'].endswith('.jpeg')):
            imgs.append(img['src'])


    ## nombres de users par Villes francaises

    df_list = pd.read_html(page.text)
    df = df_list[0]

    if not os.path.exists('./assets'):
        os.makedirs('assets')

    x =df['Agglomération'].tolist()
    y = df['Dev / 1000 habitants'].tolist()
    fig, ax = plt.subplots()
    width = 0.5
    ind = np.arange(len(y))
    ax.barh(ind, y, width, color="blue")
    ax.set_yticks(ind+width/2)
    ax.set_yticklabels(x, minor=False)
    plt.title('Pourcentage du nombre de dev par agglomération')
    plt.xlabel('Pourcentage')
    plt.ylabel('Agglomération')
    for i, v in enumerate(y):
        ax.text(v, i + .20, str(v), color='blue', fontweight='bold')
    plt.savefig('./assets/bar.png', format='png', bbox_inches='tight')

    m =df['Agglomération'].tolist()
    n = df['# GitHub'].tolist()
    fig, bx = plt.subplots()
    width = 0.5
    ind = np.arange(len(n))
    bx.barh(ind, n, width, color="blue")
    bx.set_yticks(ind+width/2)
    bx.set_yticklabels(m, minor=False)
    plt.title("Nombre d'utilisateur GitHub par agglomération")
    plt.xlabel("Nombre d'utilisateur GitHub")
    plt.ylabel('Agglomération')
    for i, v in enumerate(n):
        bx.text(v, i + .20, str(v), color='blue', fontweight='bold')
    plt.savefig('./assets/hist.png', format='png', bbox_inches='tight')
    return render_template('infos.html', images = imgs)


if __name__ == '__main__' :
    app.run(debug = True)
