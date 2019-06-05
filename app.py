from flask import Flask, url_for

app = Flask(__name__)

@app.route('/')
@app.route('/index')
@app.route('/home')
def hello_world():
    # return 'Welcome to My Watchlist'
    return '<h1>Hellow Totoro!</h1><img src="http://helloflask.com/totoro.gif">'

@app.route('/')
def hello():
    return "hellow"

@app.route('/user/<name>')
def user_page(name):
    # return "User page"
    return "User:%s" % name

@app.route('/test')
def test_url_for():
    print(url_for("hello"))

    print(url_for('user_page',name='bluesky'))

    print(url_for('user_page',name='peter'))

    print(url_for("test_url_for"))

    print(url_for('test_url_for',num=2))

    return 'Test page'

if __name__ == '__main__':
    app.run()
