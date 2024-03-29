import os
import sys
from sys import prefix

from flask import Flask, config
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy

WIN = sys.platform.startswith("win")
if WIN:  # 如果是win系统，三条斜线
    prefix = "sqlite:///"
else:  # 其他则四条斜线
    prefix = "sqlite:////"

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY','dev')
app.config['SQLALCHEMY_DATABASE_URI'] = prefix + os.path.join(os.path.dirname(app.root_path),os.getenv('DATABASE_FILE','data.db'))
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
print(app.config['SQLALCHEMY_DATABASE_URI'])
db = SQLAlchemy(app)
login_manager = LoginManager(app)

@login_manager.user_loader
def load_user(user_id):
    from watchlist.models import User
    user = User.query.get(int(user_id))
    return user

login_manager.login_view='login'

@app.context_processor
def inject_user():
    from watchlist.models import User
    user = User.query.first()
    return dict(user=user)

from watchlist import view,errors,commands

