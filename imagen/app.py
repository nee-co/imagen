import os

from flask import Flask
from flask_restful import Api

from imagen.resources.image import ImageAPI


app = Flask(__name__)
api = Api(app)


app.config.update(dict(
    UPLOAD_DIRECTORY='/srv/imagen/images/',
    ALLOWED_EXTENSIONS=('png', 'jpg', 'gif'),
    ALLOWED_FORMATS=('PNG', 'JPEG', 'GIF'),
    SAVE_EXTENSION='png',
    SAVE_FORMAT='PNG',

    MAX_CONTENT_LENGTH=32 * 2048 * 2048
))

if not os.path.exists(app.config['UPLOAD_DIRECTORY']):
    os.makedirs(app.config['UPLOAD_DIRECTORY'])

api.add_resource(ImageAPI, '/internal/images/', '/internal/images/<string:image_name>')
