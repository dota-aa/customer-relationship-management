from io import BytesIO
from PIL import Image, UnidentifiedImageError
from django.core.exceptions import ValidationError
from django.core.files.base import ContentFile


ALLOWED_IMAGE_FORMAT = ('JPG', 'JPEG', 'PNG', 'WEBP')
MAX_IMAGE_SIZE = 3 * 1024 * 1024  # 3mb


def file_upload_path(instance, filename: str) -> str:
    ext = filename.split('.')[-1]
    if ext.upper() not in ALLOWED_IMAGE_FORMAT:
        ext = 'jpg'
    return f'users/avatar/{instance.user.username}.{ext}'


def validate_avatar(file):
    if file.size > MAX_IMAGE_SIZE:
        raise ValidationError('File size must be under 3mb')

    try:
        img = Image.open(file)
        img.verify()
    except (OSError, UnidentifiedImageError):
        raise ValidationError('Invalid image.')
    finally:
        file.seek(0)

    img = Image.open(file)
    if img.format not in ALLOWED_IMAGE_FORMAT:
        raise ValidationError('Only jpg, jpeg, png and webp are allowed image formats')

    width, height = img.size
    if width > 1000 or height > 1000:
        raise ValidationError('Image is too large')
    file.seek(0)


def process_image(file):
    try:
        img = Image.open(file)

        if img.mode in ('RGBA', 'P'):
            img = img.convert('RGB')

        img.thumbnail((512, 512))

        output = BytesIO()
        img.save(output, format='jpeg', quality=85, optimize=True)
        output.seek(0)
        filename = f'WillBeSetLater.jpeg'
        return ContentFile(output.read(), name=filename)
    except Exception:
        raise ValidationError('Failed to process the image.')
