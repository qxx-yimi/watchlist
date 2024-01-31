from flask import Flask, url_for, render_template
from markupsafe import escape
from flask_sqlalchemy import SQLAlchemy
import os
import click

app = Flask(__name__)
# 先加载配置
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(app.root_path, 'data.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # 关闭对模型修改的监控
db = SQLAlchemy(app)


# database model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20))


class Movie(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(60))
    year = db.Column(db.String(4))


@app.route('/')
def index():
    user = User.query.first()
    movies = Movie.query.all()
    return render_template('index.html', user=user, movies=movies)


@app.route('/user/<name>')
def user_page(name):
    return 'User page:' + escape(name)  # escape将name进行转义处理，浏览器不会将返回的字符串作为代码执行。


@app.route('/test')
def test_url_for():
    # 下面是一些调用示例（请访问 http://localhost:5000/test 后在命令行窗口查看输出的 URL）：
    print(url_for('index'))  # 生成 hello 视图函数对应的 URL，将会输出：/
    # 注意下面两个调用是如何生成包含 URL 变量的 URL 的
    print(url_for('user_page', name='greyli'))  # 输出：/user/greyli
    print(url_for('user_page', name='peter'))  # 输出：/user/peter
    print(url_for('test_url_for'))  # 输出：/test
    # 下面这个调用传入了多余的关键字参数，它们会被作为查询字符串附加到 URL 后面。
    print(url_for('test_url_for', num=2))  # 输出：/test?num=2
    return 'Test page'


@app.cli.command() # 注册为命令
@click.option('--drop', is_flag=True, help='Create after app.')
def initdb(drop):
    if drop:
        db.drop_all()
    db.create_all()
    click.echo("Initialized database.")


@app.cli.command()
def forge():
    db.create_all()
    name = 'one meter'
    movies = [
        {'title': '我的邻居托托罗', 'year': '1988'},
        {'title': '死亡诗社', 'year': '1989'},
        {'title': '完美世界', 'year': '1993'},
        {'title': '这个杀手不太冷', 'year': '1994'},
        {'title': '麻将', 'year': '1996'},
        {'title': '燕尾蝶', 'year': '1996'},
        {'title': '喜剧之王', 'year': '1999'},
        {'title': '鬼子来了', 'year': '1999'},
        {'title': '机器人总动员', 'year': '2008'},
        {'title': '音乐之猪', 'year': '2012'},
    ]
    user = User(name=name)
    db.session.add(user)
    for m in movies:
        movie = Movie(title=m['title'], year=m['year'])
        db.session.add(movie)
    db.session.commit()
    click.echo('Done.')
