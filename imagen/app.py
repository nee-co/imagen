import os
import re
import uuid

from bottle import request
from bottle import HTTPResponse
from bottle import post
from bottle import put
from bottle import delete
from bottle import run
import magic


# Default setting value
conf = {
    'host': '0.0.0.0',
    'port': '8000',
    # ToDo: 返すURLを '/image/<UUID>' か 'image/<UUID>' のどちらにするか検討
    'image_url': '/image/',
    'image_save_directory': '/srv/imagen/images/',
}

VALID_IMAGE_EXTENSION_LIST = ('jpeg', 'jpg', 'png', 'gif')
VALID_IMAGE_MIME_LIST = ('image/png', 'image/jpeg', 'image/gif')


# ToDo: オプションとコンフィグファイルに対応させる
# import argparse, optparse
# import configparser


# Initialization
if not os.path.exists(conf['image_save_directory']):
    os.makedirs(conf['image_save_directory'])


# ToDo: コンフィグもうちょっとまともにする
ENV_IMAGEN_HOST = 'IMAGEN_HOST'
ENV_IMAGEN_PORT = 'IMAGEN_PORT'
ENV_IMAGEN_IMAGE_URL = 'IMAGEN_IMAGE_URL'
ENV_IMAGEN_IMAGE_SAVE_DIRECTORY = 'IMAGEN_IMAGE_DIRECTORY'

if os.environ.get(key=ENV_IMAGEN_HOST, default=None) is not None:
    conf['host'] = os.environ.get(ENV_IMAGEN_HOST)
if os.environ.get(key=ENV_IMAGEN_PORT, default=None) is not None:
    conf['port'] = os.environ.get(ENV_IMAGEN_PORT)
if os.environ.get(key=ENV_IMAGEN_IMAGE_URL, default=None) is not None:
    conf['image_url'] = os.environ.get(ENV_IMAGEN_IMAGE_URL)
if os.environ.get(key=ENV_IMAGEN_IMAGE_SAVE_DIRECTORY, default=None) is not None:
    conf['image_save_directory'] = os.environ.get(ENV_IMAGEN_IMAGE_SAVE_DIRECTORY)


class ImageFormatError(Exception):
    def __init__(self):
        pass


def is_valid_image_extension(image_filename):
    return True if re.findall("(?!.*\.).+", image_filename)[-1] in VALID_IMAGE_EXTENSION_LIST else False


def is_valid_image_format(image_file):
    image_file.seek(0)
    _mime = magic.from_buffer(image_file.read(), mime=True)
    return True if _mime in VALID_IMAGE_MIME_LIST else False


def generate_image_file_extension(image_file):
    image_file.seek(0)
    _mime = magic.from_buffer(image_file.read(), mime=True)
    if _mime == 'image/png':
        return 'png'
    elif _mime == 'image/jpeg':
        return 'jpg'
    elif _mime == 'image/gif':
        return 'gif'
    else:
        raise ImageFormatError


# https://imagen.neec.ooo/internal/images/<UUID>.jpg:large みたいにすればいいのでは？
@post('/internal/images')
def do_upload():
    _image = request.files.get(key='image', default=None)

    # Check None of image param
    if _image is None:
        _body = {"error": "image param is required"}
        return HTTPResponse(body=_body, status=400)

    # Check if the image param is jpeg, jpg, png, gif
    if not is_valid_image_extension(_image.filename):
        _body = {"error": "The image param must be jpeg, jpg, png, gif"}
        return HTTPResponse(body=_body, status=422)

    # Image format check
    if not is_valid_image_format(_image.file):
        _body = {"error": "Invalid image format"}
        return HTTPResponse(body=_body, status=422)

    # Create UUID
    # ToDo: 拡張子を含めずに検査するように変更
    # 非情に汚い
    try:
        while True:
            _image_filename = '{uuid}.{extension}'.format(uuid=str(uuid.uuid4()), extension=generate_image_file_extension(_image.file))

            # ファイル名が被っていたらUUIDを作成し直す
            if not os.path.exists('{dir}/{name}'.format(dir=conf['image_save_directory'], name=_image_filename)):
                break

    except ImageFormatError:
        _body = {"error": "Invalid image format"}
        return HTTPResponse(body=_body, status=422)

    # Save image
    _image.file.seek(0)
    _image.save('{dir}/{name}'.format(dir=conf['image_save_directory'], name=_image_filename))

    _body = {"image_path": "{path}{name}".format(path=conf['image_url'], name=_image_filename)}
    res = HTTPResponse(body=_body, status=201)
    return res


@put('/internal/images/<image_name>')
def do_put(image_name):

    # ToDo: ディレクトリトラバーサル的な対策
    # 正規表現で「~」と「..」「$」「\」「'」「"」無効化すれば良さそう

    # ToDo: 上書き元のファイルが存在しない場合の挙動をどうするか検討
    # 現在は存在しなくても更新可能

    _image = request.files.get(key='image', default=None)

    # Check None of image param
    if _image is None:
        _body = {"error": "image param is required"}
        return HTTPResponse(body=_body, status=400)

    # Check if the image param is jpeg, jpg, png, gif
    if not is_valid_image_extension(_image.filename):
        _body = {"error": "The image param must be jpeg, jpg, png, gif"}
        return HTTPResponse(body=_body, status=422)

    # Image format check
    if not is_valid_image_format(_image.file):
        _body = {"error": "Invalid image format"}
        return HTTPResponse(body=_body, status=422)

    _path = '{dir}/{name}'.format(dir=conf['image_save_directory'], name=image_name)

    # ToDo: 元のファイル名と、新たに送信したファイル名の拡張子が違う場合に元のファイルを削除する
    # 現状は上書きするimageのMIME typeに関わらず、既にアップロード済みの拡張子が使用される
    # 拡張子を変更してしまうと他システムでDBに格納されている画像pathが変わってしまい、
    # わざわざPUTを用意した意味が無くなってしまう
    # ToDo: 仕様の再検討

    try:
        _image.file.seek(0)
        _image.save(_path, overwrite=True)
    except Exception as e:
        print(e)
        return HTTPResponse(status=500)

    _body = {"image_path": "{path}{name}".format(path=conf['image_url'], name=image_name)}
    res = HTTPResponse(body=_body, status=200)
    return res


@delete('/internal/images/<image_name>')
def do_delete(image_name):

    # ToDo: ディレクトリトラバーサル的な対策
    # 正規表現で「~」と「..」「$」「\」「'」「"」無効化すれば良さそう

    _path = '{dir}/{name}'.format(dir=conf['image_save_directory'], name=image_name)

    # ToDo: ファイルが存在しなかった場合の挙動をどうするか検討

    if not os.path.exists(_path):
        print('{image_name} not exists'.format(image_name=image_name))
        return HTTPResponse(status=404)

    if os.path.isdir(_path):
        print('{image_name} is Directory'.format(image_name=image_name))
        return HTTPResponse(status=422)

    try:
        os.remove(_path)
    except Exception as e:
        print(e)
        return HTTPResponse(status=500)

    res = HTTPResponse(status=204)
    return res


run(host=conf['host'], port=conf['port'])
