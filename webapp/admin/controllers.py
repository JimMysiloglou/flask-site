from .forms import LoginForm, AccountUpdateForm, CKTextAreaField
from flask_admin.contrib.sqla import ModelView
from flask_admin import expose, AdminIndexView
from flask_login import login_required, current_user, login_user, logout_user
from PIL import Image
import os, secrets
from flask import flash, redirect, url_for, abort
from .. import db
from webapp.auth.models import User
from flask_admin.form import SecureForm, ImageUploadField



# The size variable is a tuple like (640, 480)
def image_save(image, where, size):
    random_filename = secrets.token_hex(12)
    _, file_extension = os.path.splitext(image.filename)
    image_filename = random_filename + file_extension
    image_path = os.path.join('../static', 'images', where, image_filename)

    img = Image.open(image)
    img.thumbnail(size)
    img.save(image_path)

    return image_filename

# Create customized model view class
class CustomModelView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated


# Create customized index view class that handles login & registration
class MyAdminIndexView(AdminIndexView):

    @expose('/')
    @login_required
    def index(self):
        return super(MyAdminIndexView, self).index()

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
        return super(MyAdminIndexView, self).index()


    @expose('/edit_acount/', methods=["GET", "POST"])
    @login_required
    def edit_acount_view(self):
        form  = AccountUpdateForm(name=current_user.name,
                                  email=current_user.email,
                                  password=current_user.password,
                                  profile_image=current_user.profile_image)

        if form.validate_on_submit():
            current_user.name = form.name.data
            current_user.email = form.email.data

            if not current_user.verify_password(form.password.data):
                current_user.password = form.password.data

            if form.profile_image not in ['default_profile_image.jpg', current_user.profile_image]:
                try:
                    profile_image = image_save(form.profile_image.data, 'profile_images', (350, 350))
                except BaseException as err:
                    abort(415)

            db.session.commit()
            flash(f"The account for user <b>{current_user.name}</b> has updated successfully", "success")

            return redirect(url_for('.index'))

        self._template_args['form'] = form
        return super(MyAdminIndexView, self).index()

    @expose('/logout/')
    def logout_view(self):
        logout_user()
        return redirect(url_for('.index'))


def prefix_name(obj, file_data):
    random_filename = secrets.token_hex(12)
    _, file_extension = os.path.splitext(file_data.filename)
    return random_filename + file_extension


class UserAdminView(CustomModelView):
    form_overrides = dict(profile_image=ImageUploadField)
    form_args = dict(profile_image={'base_path': 'static/images/profile_images', 'namegen':prefix_name, 'url_relative_path':'images/profile_images/'})
    form_base_class = SecureForm


class ArticleAdminView(CustomModelView):
    form_overrides = dict(article_body=CKTextAreaField, article_image=ImageUploadField)
    form_args = dict(article_image={'base_path': 'static/images/article_images', 'namegen':prefix_name, 'url_relative_path':'images/article_images/'})
    form_base_class = SecureForm
    create_template = 'admin/edit_article.html'
    edit_template = 'admin/edit_article.html'


class ProjectAdminView(CustomModelView):
    form_overrides = dict(project_body=CKTextAreaField, project_image=ImageUploadField)
    form_args = dict(project_image={'base_path': 'static/images/project_images', 'namegen':prefix_name, 'url_relative_path':'images/project_images/'})
    form_base_class = SecureForm
    create_template = 'admin/edit_project.html'
    edit_template = 'admin/edit_project.html'