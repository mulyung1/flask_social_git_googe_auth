import os

from flask import Flask, jsonify, redirect, url_for, render_template
from flask_dance.contrib.github import github
from flask_login import logout_user, login_required
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from app.models import db, login_manager
from app.oauth import github_blueprint

os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

app=Flask(__name__)
app.secret_key='secret'
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///users.db'
app.register_blueprint(github_blueprint, url_prefix='/login')

#db = SQLAlchemy(app)
migrate = Migrate(app, db)

db.init_app(app)
login_manager.init_app(app)

with app.app_context():
    db.create_all()

OAUTHLIB_INSECURE_TRANSPORT='1'

@app.route('/ping')
def ping():
    return jsonify(ping='pong')

@app.route('/')
def homepage():
    return render_template('index.html')

@app.route('/profile')
def profile():
    return render_template('profile.html')

@app.route('/github')
def login():
    if not github.authorized:
        return redirect(url_for('github.login'))
    res=github.get('/user')
    username = res.json()["login"]

    #return f"You are @{username} on GitHub"
    return redirect(url_for('profile')) 

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('homepage'))

if __name__ == '__main__':
    app.run(debug=True, port=5000)