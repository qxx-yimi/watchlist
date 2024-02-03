import click

from watchlist import db, app
from watchlist.models import Movie, User


@app.cli.command()  # 注册为命令
@click.option('--drop', is_flag=True, help='Create after app.')
def initdb(drop):
    if drop:
        db.drop_all()
    db.create_all()
    click.echo("Initialized database.")


@app.cli.command()
def forge():
    # db.create_all()
    # name = 'one meter'
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
    # user = User(name=name)
    # db.session.add(user)
    for m in movies:
        movie = Movie(title=m['title'], year=m['year'])
        db.session.add(movie)
    db.session.commit()
    click.echo('Done.')


@app.cli.command()
@click.option('--username', prompt=True, help='The username used to login.')
@click.option('--password', prompt=True, hide_input=True, confirmation_prompt=True)
def admin(username, password):
    db.create_all()
    user = User.query.first()
    if user is not None:
        click.echo('Updating user...')
        user.username = username
        user.set_password(password)
    else:
        click.echo('Creating user...')
        user = User(username=username, name='meter')
        user.set_password(password)
        db.session.add(user)

    db.session.commit()
    click.echo('Done.')
