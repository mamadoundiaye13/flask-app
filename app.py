from flask import render_template, url_for, Flask, redirect
import requests
from config import Config
from form import IndexForm

app = Flask(__name__)
app.config.from_object(Config)

@app.route('/', methods=['POST', 'GET'])
def index():
    form = IndexForm()
    if form.validate_on_submit():
        return redirect(url_for('getUser', name=form.username.data))

    return render_template('index.html', title='Username', form=form)

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
    responseFollowings = requests.get(urlFollowers)
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

    elif response.headers['X-RateLimit-Remaining'] == str(0):
        return render_template('error.html',
            status_code = response.status_code,
            limit = int(response.headers['X-RateLimit-Remaining']),
            response = response.json()
            )

@app.route('/repos/<name>')
def getOneRepos(name=None):
    return render_template('one-repos.html', name=name)

if __name__ == '__main__' :
    app.run(debug = True)
