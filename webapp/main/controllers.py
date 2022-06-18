from flask import Blueprint, redirect, render_template, flash, url_for
from webapp.blog.models import Article
from webapp.main.forms import ContactForm
from .models import Message, db
from flask_babel import _

main_blueprint = Blueprint(
    'main',
    __name__,
    template_folder='../templates/main'
)

@main_blueprint.route('/')
def index():
    return render_template('index.html')


from .forms import SearchForm

@main_blueprint.app_context_processor
def inject_searchform():
    form = SearchForm()
    return dict(form=form)


@main_blueprint.route("/search/", methods=["POST"])
def search():
    form = SearchForm()

    if form.validate_on_submit():
        searched_string = form.searched.data

        articles = Article.query.filter(Article.article_body.contains(searched_string))
        articles = articles.order_by(Article.date_created)

        return render_template("search.html", articles=articles, searched=searched_string)

    


@main_blueprint.route("/contact/", methods=["GET", "POST"])
def contact():
    form = ContactForm()

    if form.validate_on_submit():
        name = form.name.data
        email = form.email.data
        message = form.message.data

        message = Message(name=name, email=email, message=message)

        db.session.add(message)
        db.session.commit()

        flash(_("Your message has submitted succesfully"), "success")
        return redirect(url_for("main.contact"))

    return render_template("contact.html", form=form)

@main_blueprint.app_errorhandler(403)
def forbidden(e):
    return render_template('errors/403.html'), 403

@main_blueprint.app_errorhandler(404)
def page_not_found(e):
    return render_template('errors/404.html'), 404

@main_blueprint.app_errorhandler(415)
def unsupported_media_type(e):
    return render_template('errors/415.html'), 415

@main_blueprint.app_errorhandler(500)
def internal_server_error(e):
    return render_template('errors/500.html'), 500