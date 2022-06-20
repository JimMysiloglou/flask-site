from flask import (
    render_template,
    Blueprint,
    flash,
    redirect,
    session,
    url_for,
    request
)
from .models import Article, Comment, Tag, db
from .forms import CommentForm
from flask_babel import _

blog_blueprint = Blueprint(
    'blog',
    __name__,
    template_folder='../templates/blog',
    url_prefix="/blog"
)

@blog_blueprint.route('/')
def blog():
    page = request.args.get("page", 1, type=int)
    lang = session['locale'] or 'el'
    
    first_article = None
    if page == 1:
        first_article = Article.query.filter_by(language_id=lang).order_by(Article.date_created.desc()).first()

    articles = Article.query.filter_by(language_id=lang).order_by(Article.date_created.desc()).offset(1).from_self().paginate(per_page=6, page=page)

    tags = Tag.query.all()

    return render_template("blog.html", first_article=first_article, articles=articles, tags=tags)


@blog_blueprint.route("/articles_by_tag/<int:tag_id>")
def articles_by_tag(tag_id):
    page = request.args.get("page", 1, type=int)
    
    tag = Tag.query.get(tag_id)
    tags = Tag.query.all()
    
    lang = session['locale'] or 'el'
    articles = Article.query.filter_by(language_id=lang).with_parent(tag).order_by(Article.date_created.desc()).paginate(per_page=4, page=page)
    
    return render_template("articles_by_tag.html", articles=articles, main_tag=tag, tags=tags, page=page)


@blog_blueprint.route("/full_article/<int:article_id>", methods=["GET", "POST"])
def full_article(article_id):
    article = Article.query.get_or_404(article_id)

    form = CommentForm()
    if form.validate_on_submit():
        comment_author = form.author.data
        comment_email = form.email.data
        comment_text = form.text.data

        comment = Comment(author=comment_author,
                            email=comment_email,
                            text=comment_text,
                            article_id=article.id)

        db.session.add(comment)
        db.session.commit()

        flash(_("The comment has posted successfully"), "success")
        return redirect(url_for("blog.full_article", article_id=article_id, _anchor='comments'))
    
    return render_template("full_article.html", article=article, form=form)