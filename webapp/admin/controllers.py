from .forms import LoginForm, CKTextAreaField
from flask_admin.contrib.sqla import ModelView
from flask_admin import expose, AdminIndexView
from flask_login import login_required, current_user, login_user, logout_user
import os, secrets
from flask import flash, redirect, url_for
from .. import db
from webapp.auth.models import User
from flask_admin.form import SecureForm, ImageUploadField
from flask_admin.contrib.fileadmin import FileAdmin


# Create customized model view class
class CustomModelView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated


# Create customized index view class that handles login & registration
class MyAdminIndexView(AdminIndexView):

    @expose('/')
    @login_required
    def index(self):
        return self.render('admin/index.html')

    @expose('/login/', methods=['GET', 'POST'])
    def login_view(self):
        form = LoginForm()
        if form.validate_on_submit():
            email = form.email.data
            password = form.password.data

            if user := User.query.filter_by(email=email).first():
                if user.verify_password(password):
                    flash(f"The user with email: {email} has signed in successfully", "success")
                    login_user(user, remember=form.remember_me.data)
            else:
                flash("There is no user with that email", "warning")
        
        if current_user.is_authenticated:
            return redirect(url_for('.index'))

        self._template_args['form'] = form
        return self.render('admin/index.html')
    
    @expose('/logout/')
    def logout_view(self):
        logout_user()
        return redirect(url_for('.index'))




def prefix_name(obj, file_data):
    random_filename = secrets.token_hex(12)
    _, file_extension = os.path.splitext(file_data.filename)
    return random_filename + file_extension



class ArticleAdminView(CustomModelView):
    form_base_class = SecureForm
    form_overrides = {
        'article_image': ImageUploadField,
        'article_body': CKTextAreaField
    }
    form_args = {
        'article_image': {
            'label': 'Image',
            'base_path': 'webapp/static/images/article_images/',
            'allow_overwrite': False,
            'url_relative_path':'images/article_images/',
            'namegen': prefix_name
        }
    }
    column_exclude_list = ('article_body',)
    column_searchable_list = ('article_title', 'article_description')
    column_filters = ('date_created',)
    create_template = 'admin/edit_article.html'
    edit_template = 'admin/edit_article.html'


class ProjectAdminView(CustomModelView):
    form_base_class = SecureForm
    form_overrides = {
        'project_image': ImageUploadField,
        'project_body': CKTextAreaField
    }
    form_args = {
        'project_image': {
            'label': 'Image',
            'base_path': 'webapp/static/images/project_images/',
            'allow_overwrite': False,
            'url_relative_path':'images/project_images/',
            'namegen': prefix_name
        }
    }
    column_exclude_list = ('project_body',)
    column_searchable_list = ('project_title', 'project_description')
    column_filters = ('date_created',)
    create_template = 'admin/edit_project.html'
    edit_template = 'admin/edit_project.html'

class CustomFileAdmin(FileAdmin):
    def is_accessible(self):
        return current_user.is_authenticated