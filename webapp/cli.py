import logging
from random import sample, choice
import click
from .auth.models import User, db
from .blog.models import Article, Tag
from .portfolio.models import Project
from faker import Faker

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
    @app.cli.command('create-user')
    @click.argument('name')
    @click.argument('email')
    @click.argument('password')
    def create_user(name, email, password):
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
    def text_data():
        generate_articles(50, generate_tags(15))
        generate_projects(15)