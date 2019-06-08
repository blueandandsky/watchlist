import os
import sys

import click
from flask import Flask, url_for, render_template
from flask_sqlalchemy import SQLAlchemy

WIN = sys.platform.startswith("win")
if WIN:  # 如果是win系统，三条斜线
    prefix = "sqlite:///"
else:  # 其他则四条斜线
    prefix = "sqlite:////"
app = Flask(__name__)

# 2chapter
# @app.route('/')
# @app.route('/index')
# @app.route('/home')
# def hello_world():
# return 'Welcome to My Watchlist'
# return '<h1>Hellow Totoro!</h1><img src="http://helloflask.com/totoro.gif">'

# @app.route('/')
# def hello():
#     return "hellow"
#
# @app.route('/user/<name>')
# def user_page(name):
#     # return "User page"
#     return "User:%s" % name
#
# @app.route('/test')
# def test_url_for():
#     print(url_for("hello"))
#
#     print(url_for('user_page',name='bluesky'))
#
#     print(url_for('user_page',name='peter'))
#
#     print(url_for("test_url_for"))
#
#     print(url_for('test_url_for',num=2))
#
#     return 'Test page'

# 3chapter
# name = "bluesky"
# movies = [{'title': 'My Meighbor Totoro', 'year': '1988'},
#           {'title': 'Dead Poets Society', 'year': '1989'},
#           {'title': 'A Perfect World', 'year': '1993'},
#           {'title': 'Leon', 'year': '1994'},
#           {'title': 'Mahjong', 'year': '1996'},
#           {'title': 'Swallowtail Butterfly', 'year': '1996'},
#           {'title': 'King of Comedy', 'year': '1999'},
#           {'title': 'Devils on the Doorstep', 'year': '1999'},
#           {'title': 'WALL-E', 'year': '2008'},
#           {'title': 'The Pork of Music', 'year': '2012'}]
#
#
# @app.route('/')
# def index():
#     return render_template('index.html', name=name, movies=movies)

# 5chapter
app.config['SQLALCHEMY_DATABASE_URI'] = prefix + os.path.join(app.root_path, 'data.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # 关闭对模型修改的监控
# 在扩展类实例化前加载配置
db = SQLAlchemy(app)


class User(db.Model):  # 表明user，自动生成 小写处理
    id = db.Column(db.Integer, primary_key=True)  # 主键
    name = db.Column(db.String(20))  # 名字


class Movie(db.Model):  # 表名movie
    id = db.Column(db.Integer, primary_key=True)  # 主键
    title = db.Column(db.String(60))  # 电影标题
    year = db.Column(db.String(4))  # 电影年份


@app.cli.command()
@click.option('--drop', is_flag=True, help='Create after drop.')
def initdb(drop):
    if drop:
        db.drop_all()
    db.create_all()
    click.echo("Initizlized database.")

# @app.route('/')
# def index():
#     user = User.query.first()
#     movies = Movie.query.all();
#     return render_template('index.html', user=user, movies=movies)


# @app.cli.command()
# def forge():
#     db.create_all()
#
#     name = "bluesky"
#     movies = [{'title': 'My Meighbor Totoro', 'year': '1988'},
#               {'title': 'Dead Poets Society', 'year': '1989'},
#               {'title': 'A Perfect World', 'year': '1993'},
#               {'title': 'Leon', 'year': '1994'},
#               {'title': 'Mahjong', 'year': '1996'},
#               {'title': 'Swallowtail Butterfly', 'year': '1996'},
#               {'title': 'King of Comedy', 'year': '1999'},
#               {'title': 'Devils on the Doorstep', 'year': '1999'},
#               {'title': 'WALL-E', 'year': '2008'},
#               {'title': 'The Pork of Music', 'year': '2012'}]
#
#     user = User(name=name)
#     db.session.add(user)
#     for m in movies:
#         movie = Movie(title=m['title'], year=m['year'])
#         db.session.add(movie)
#
#     db.session.commit()
#     click.echo('Done.')

# 6chapter
# @app.errorhandler(404)
# def page_not_found(e):
#     user = User.query.first();
#     return render_template('404.html',user=user),404

@app.context_processor
def inject_user():
    user=User.query.first()
    return dict(user=user)

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'),404

@app.route('/')
def index():
    movies = Movie.query.all()
    return render_template('index.html', movies=movies)

if __name__ == '__main__':
    app.run()
