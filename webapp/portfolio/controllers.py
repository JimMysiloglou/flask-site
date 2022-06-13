from crypt import methods
from flask import (render_template,
    Blueprint,
    flash,
    redirect,
    url_for
)
from .models import Project, db
from webapp.blog.models import Comment
from webapp.blog.forms import CommentForm

portfolio_blueprint = Blueprint(
    'portfolio',
    __name__,
    template_folder='../templates/portfolio',
    url_prefix="/portfolio"
)

@portfolio_blueprint.route('/')
def portfolio():
    projects  = Project.query.order_by(Project.date_created.desc()).all()
    return render_template("portfolio.html", projects=projects)


@portfolio_blueprint.route('/full_project/<int:project_id>', methods=['GET', 'POST'])
def full_project(project_id):
    project = Project.query.get_or_404(project_id)

    form = CommentForm()
    if form.validate_on_submit():
        comment_author = form.author.data
        comment_email = form.email.data
        comment_text = form.text.data

        comment = Comment(author=comment_author,
                            email=comment_email,
                            text=comment_text,
                            project_id=project.id)


        db.session.add(comment)
        db.session.commit()

        flash("The comment has posted successfully", "success")
        return redirect(url_for("portfolio.full_project", project_id=project_id, _anchor='comments'))

    return render_template("full_project.html", project=project, form=form)