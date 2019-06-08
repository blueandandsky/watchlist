import os
import sys

import click
from flask import Flask, url_for, render_template, request, flash, redirect
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

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
app.config['SECRET_KEY'] = 'dev'
app.config['SQLALCHEMY_DATABASE_URI'] = prefix + os.path.join(app.root_path, 'data.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # 关闭对模型修改的监控
# 在扩展类实例化前加载配置
db = SQLAlchemy(app)


class User(db.Model, UserMixin):  # 表明user，自动生成 小写处理
    id = db.Column(db.Integer, primary_key=True)  # 主键
    name = db.Column(db.String(20))  # 名字
    username = db.Column(db.String(20))
    password_hash = db.Column(db.String(128))

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def validate_password(self, password):
        return check_password_hash(self.password_hash,password)


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


@app.cli.command()
def forge():
    db.create_all()

    name = "bluesky"
    movies = [{'title': 'My Meighbor Totoro', 'year': '1988'},
              {'title': 'Dead Poets Society', 'year': '1989'},
              {'title': 'A Perfect World', 'year': '1993'},
              {'title': 'Leon', 'year': '1994'},
              {'title': 'Mahjong', 'year': '1996'},
              {'title': 'Swallowtail Butterfly', 'year': '1996'},
              {'title': 'King of Comedy', 'year': '1999'},
              {'title': 'Devils on the Doorstep', 'year': '1999'},
              {'title': 'WALL-E', 'year': '2008'},
              {'title': 'The Pork of Music', 'year': '2012'}]

    user = User(name=name)
    db.session.add(user)
    for m in movies:
        movie = Movie(title=m['title'], year=m['year'])
        db.session.add(movie)

    db.session.commit()
    click.echo('Done.')

# 6chapter
# @app.errorhandler(404)
# def page_not_found(e):
#     user = User.query.first();
#     return render_template('404.html',user=user),404

@app.context_processor
def inject_user():
    user = User.query.first()
    return dict(user=user)


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


# @app.route('/')
# def index():
#     movies = Movie.query.all()
#     return render_template('index.html', movies=movies)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == "POST":
        # 8chapter
        if not current_user.is_authenticated:
            return redirect(url_for('index'))


        title = request.form.get('title')
        year = request.form.get('year')

        if not title or not year or len(year) > 4 or len(title) > 60:
            flash('Invalid input')
            return redirect(url_for('index'))

        movie = Movie(title=title, year=year)
        db.session.add(movie)
        db.session.commit()
        flash('Item created')
        return redirect(url_for('index'))
    user = User.query.first()
    movies = Movie.query.all()
    return render_template('index.html', user=user, movies=movies)


# 7chapter
@app.route('/movie/edit/<int:movie_id>', methods=['GET', 'POST'])
@login_required
def edit(movie_id):
    movie = Movie.query.get_or_404(movie_id)

    if request.method == "POST":
        title = request.form['title']
        year = request.form['year']

        if not title or not year or len(year) > 4 or len(title) > 60:
            flash('Invlaid input.')
            return redirect(url_for('edit', movie_id=movie_id))

        movie.title = title
        movie.year = year
        db.session.commit()
        flash('Item updated.')
        return redirect(url_for('index'))

    return render_template('edit.html', movie=movie)


@app.route('/movie/delete/<int:movie_id>', methods=['POST'])
@login_required
def delete(movie_id):
    movie = Movie.query.get_or_404(movie_id)
    db.session.delete(movie)
    db.session.commot()
    flash('Item deleted.')
    return redirect(url_for('index'))


# 8chapter
@app.cli.command()
@click.option('--username', prompt=True, help='The username used to login.')
@click.option('--password', prompt=True, hide_input=True, confirmation_prompt=True, help='The password used to login.')
def admin(username, password):
    db.create_all()

    user = User.query.first()

    if user is not None:
        click.echo('Updating user...')
        user.username = username
        user.set_password(password)
    else:
        click.echo('Creating user...')
        user = User(username=username, name='Admin')
        user.set_password(password)
        db.session.add(user)

    db.session.commit()
    click.echo('Done.')


login_manager = LoginManager(app)
login_manager.login_view = 'login'


@login_manager.user_loader
def load_user(user_id):
    user = User.query.get(int(user_id))
    return user


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if not username or not password:
            flash('Invalid input.')
            return redirect(url_for('login'))

        user = User.query.first()

        if username == user.username and user.validate_password(password):
            login_user(user)
            flash('Login success.')
            return redirect(url_for('index'))

        flash('Invalid username or password.')
        return redirect(url_for('login'))

    return render_template('login.html')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Goodbye')
    return redirect(url_for('index'))

@app.route('/settings',methods=['GET','POST'])
@login_required
def settings():
    if request.method == 'POST':
        name = request.form['name']
        if not name or len(name) > 20:
            flash('Invalid input.')
            return redirect(url_for('settings'))

        current_user.name = name

        db.session.commit()

        flash('Settings updated.')
        return redirect(url_for('index'))

    return render_template('settings.html')

if __name__ == '__main__':
    app.run()
