from uuid import uuid4
import os

from PIL import Image
from flask import current_app
from flask import jsonify
from flask import make_response
from flask import request
from flask_restful import Resource
from werkzeug.utils import secure_filename

from imagen.common import util


class ImageAPI(Resource):
    def post(self):
        image = request.files['image']

        if not util.is_allowed_image(image):
            return make_response(jsonify({'message': 'Invalid Image'}), 422)

        pil_image = Image.open(image.stream)

        filename = ''
        file_path = '/'
        while os.path.exists(file_path):
            filename = str(uuid4()) + '.' + current_app.config['SAVE_EXTENSION']
            file_path = os.path.join(current_app.config['UPLOAD_DIRECTORY'], filename)

        pil_image.save(file_path, current_app.config['SAVE_FORMAT'])

        return make_response(jsonify({'image_name': filename}), 201)

    def put(self, image_name: str):
        if image_name.rsplit('.', 1)[1] != current_app.config['SAVE_EXTENSION']:
             return make_response(jsonify({'message': 'Invalid URL extension'}), 400)

        image = request.files['image']

        if not util.is_allowed_image(image):
            return make_response(jsonify({'message': 'Invalid Image'}), 422)

        filename = secure_filename(image_name)
        if filename != image_name:
            return make_response(jsonify({'message': 'Invalid image_name'}), 400)

        file_path = os.path.join(current_app.config['UPLOAD_DIRECTORY'], filename)

        pil_image = Image.open(image.stream)
        pil_image.save(file_path, current_app.config['SAVE_FORMAT'])

        return make_response(jsonify({'file_name': filename}), 201)

    def delete(self, image_name: str):
        filename = secure_filename(image_name)

        if filename != image_name:
            return make_response(jsonify({'message': 'Invalid image_name'}), 400)

        file_path = os.path.join(current_app.config['UPLOAD_DIRECTORY'], filename)

        try:
            os.remove(file_path)
        except FileNotFoundError:
            return make_response(jsonify({'message': 'Image Not Found'}), 404)
        except OSError:
            return make_response(jsonify({'message': 'Internal Server Error'}), 500)

        return None, 204
