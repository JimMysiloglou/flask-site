from flask_admin import Admin
from .. import db
from .controllers import CustomModelView, MyAdminIndexView, UserAdminView, ArticleAdminView
from webapp.blog.models import Article, Comment, Tag
from webapp.auth.models import User
from flask_ckeditor import CKEditor

ckeditor = CKEditor()


def create_module(app, **kwargs):
    admin = Admin(app, index_view=MyAdminIndexView(), base_template='admin/my_master.html', template_mode='bootstrap4')

    ckeditor.init_app(app)
    
    admin.add_view(UserAdminView(User, db.session))
    admin.add_view(ArticleAdminView(Article, db.session))
    admin.add_view(CustomModelView(Tag, db.session))
    admin.add_view(CustomModelView(Comment, db.session))