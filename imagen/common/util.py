from PIL import Image
from flask import current_app
from werkzeug.datastructures import FileStorage


def is_allowed_image(image: FileStorage) -> bool:
    try:
        im = Image.open(image)
    except OSError:
        return False

    # if os.path.splitext(image.filename)[1] not in current_app.config['ALLOWED_EXTENSIONS']:
    # 上の場合拡張子は '.png' になる
    # 下の場合拡張子は 'png' になる
    if image.filename.rsplit('.', 1)[1] not in current_app.config['ALLOWED_EXTENSIONS']:
        return False

    if im.format not in current_app.config['ALLOWED_FORMATS']:
        return False

    return True
