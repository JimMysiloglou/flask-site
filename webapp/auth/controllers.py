from flask import Blueprint
import os, secrets
from flask import send_from_directory, request, url_for
from flask_ckeditor import upload_fail, upload_success

auth_blueprint = Blueprint(
    'auth',
    __name__
)

# CKEditor image uploading
@auth_blueprint.route('/files/<filename>')
def uploaded_files(filename):
    path = os.path.join('../static/images', 'other_images')
    return send_from_directory(path, filename)

@auth_blueprint.route('/upload', methods=['POST'])
def upload():
    f = request.files.get('upload')
    _, extension = os.path.splitext(f.filename)
    random_filename = secrets.token_hex(12)
    if extension not in ['.jpg', '.gif', '.png', '.jpeg']:
        return upload_fail(message='Image only!')
    f.filename = random_filename + extension
    f.save(os.path.join('../static/images', 'other_images', f.filename))
    print(f.filename)
    url = url_for('uploaded_files', filename=f.filename)
    return upload_success(url, filename=f.filename)