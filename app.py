from flask import Flask, url_for, render_template
from markupsafe import escape

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html', name=name, movies=movies)


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
