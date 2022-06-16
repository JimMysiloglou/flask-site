from flask_admin import Admin
from .. import db
from .controllers import CustomModelView, MyAdminIndexView, ArticleAdminView, ProjectAdminView, CustomFileAdmin
from webapp.blog.models import Article, Comment, Tag
from webapp.auth.models import User
from webapp.portfolio.models import Project
from webapp.main.models import Message
from flask_ckeditor import CKEditor

ckeditor = CKEditor()


def create_module(app, **kwargs):
    admin = Admin(app, index_view=MyAdminIndexView(), base_template='admin/my_master.html', template_mode='bootstrap4')

    ckeditor.init_app(app)
    
    admin.add_view(CustomModelView(User, db.session))
    admin.add_view(ArticleAdminView(Article, db.session))
    admin.add_view(ProjectAdminView(Project, db.session))
    admin.add_view(CustomModelView(Tag, db.session))
    admin.add_view(CustomModelView(Comment, db.session))
    admin.add_view(CustomModelView(Message, db.session))
    admin.add_view(CustomFileAdmin(app.static_folder, '/static/', name='Static Files'))