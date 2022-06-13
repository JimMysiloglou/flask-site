from flask import Blueprint, render_template, request
from webapp.blog.models import Article

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


@main_blueprint.route("/search", methods=["POST"])
def search():
    form = SearchForm()

    page = request.args.get("page", 1, type=int)

    if form.validate_on_submit():
        searched_string = form.searched.data

        articles = Article.query.filter(Article.article_body.contains(searched_string))
        articles = articles.order_by(Article.date_created).paginate(per_page=4, page=page)

        return render_template("search.html", form=form, articles=articles, searched=searched_string, page=page)