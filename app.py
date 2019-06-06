from flask import Flask, url_for, render_template

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


@app.route('/')
def index():
    return render_template('index.html', name=name, movies=movies)


if __name__ == '__main__':
    app.run()
