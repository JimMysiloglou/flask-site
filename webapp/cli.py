import logging
from random import sample, choice
import click
from .auth.models import User, db
from .blog.models import Article, Tag
from .portfolio.models import Project
from faker import Faker
import os
from getpass import getpass
from flask_migrate import upgrade

log = logging.getLogger(__name__)

faker = Faker()


def generate_tags(n):
    tags = []
    for _ in range(n):
        tag_title = faker.color_name()
        if tag := Tag.query.filter_by(name=tag_title).first():
            tags.append(tag)
            continue
        tag_description = faker.sentence()
        tag = Tag(name=tag_title, description=tag_description)
        tags.append(tag)
        try:
            db.session.add(tag)
            db.session.commit()
        except Exception as e:
            log.error(f"Fail to add tag {str(tag)}: {e}")
            db.session.rollback()
    return tags


def generate_articles(n, tags):
    user = User.query.first()
    for _ in range(n):
        article = Article(language_id=choice(['en', 'el']),
                          article_title=faker.sentence(),
                          article_description=faker.paragraph(),
                          article_body=faker.text(max_nb_chars=1000),
                          github_link=faker.url(),
                          date_created = faker.past_date(),
                          user_id=user.id,
                          tags=[tags[i] for i in sample(range(14), 3)]
                          )
        try:
            db.session.add(article)
            db.session.commit()
        except Exception as e:
            log.error(f"Fail to add article {str(article)}, {e}")
            db.session.rollback()


def generate_projects(n):
    user = User.query.first()
    for _ in range(n):
        project = Project(language_id=choice(['en', 'el']),
                          project_title=faker.sentence(),
                          project_description=faker.paragraph(),
                          project_body=faker.text(max_nb_chars=1000),
                          github_link=faker.url(),
                          date_created=faker.past_date(),
                          user_id=user.id)
        try:
            db.session.add(project)
            db.session.commit()
        except Exception as e:
            log.error(f"Fail to add project {str(project)}, {e}")
            db.session.rollback()



def register(app):
    @app.cli.command('create-admin')
    def create_user():
        if User.query.first():
            create = input('An admin user already exists! Create another? (y/n): ')
            if create == 'n':
                return
        name = input('Enter name: ')
        email = input('Enter email: ')
        password = getpass()
        assert password == getpass('Password (again):')
        user = User(name=name, email=email, password=password)
        try:
            db.session.add(user)
            db.session.commit()
            click.echo(f"User {name} added.")
        except Exception as e:
            log.error(f"Fail to add new user: {name} Error: {e}")
            db.session.rollback()

    @app.cli.command('list-routes')
    def list_routes():
        for url in app.url_map.iter_rules():
            click.echo(f"{url.rule}, {url.methods}, {url.endpoint}")

    @app.cli.command('list-users')
    def list_users():
        try:
            users = User.query.all()
            for user in users:
                click.echo(f"{user.name}")
        except Exception as e:
            log.error(f"Fail to list users Error: {e}")
            db.session.rollback()

    @app.cli.command('test-data')
    def test_data():
        generate_articles(50, generate_tags(15))
        generate_projects(15)

    @app.cli.group()
    def translate():
        """Translation and localization commands."""
        pass

    @translate.command()
    @click.argument('lang')
    def init(lang):
        """Initialize a new language."""
        if os.system('pybabel extract -F babel/babel.cfg -k _l -o babel/messages.pot .'):
            raise RuntimeError('extract command failed')
        if os.system(f'pybabel init -i babel/messages.pot -d webapp/translations -l {lang}'):
            raise RuntimeError('init command failed')
        os.remove('babel/messages.pot')

    @translate.command()
    def update():
        """Update all languages."""
        if os.system('pybabel extract -F babel/babel.cfg -k _l -o babel/messages.pot .'):
            raise RuntimeError('extract command failed')
        if os.system('pybabel update -i babel/messages.pot -d webapp/translations'):
            raise RuntimeError('update command failed')
        os.remove('babel/messages.pot')

    @translate.command()
    def compile():
        """Compile all languages."""
        if os.system('pybabel compile -d webapp/translations'):
            raise RuntimeError('compile command failed')

    @app.cli.command('deploy')
    def deploy():
        """Run deployment tasks."""
        # migrate database to latest revision
        upgrade()
