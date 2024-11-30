from PIL import Image

from django.core.exceptions import ValidationError
from django.utils.deconstruct import deconstructible
from django.template.defaultfilters import filesizeformat


@deconstructible
class FileSizeValidator(object):
    error_messages = {
     'max_size': ("Ensure this file size is not greater than %(max_size)s."
                  " Your file size is %(size)s."),
     'min_size': ("Ensure this file size is not less than %(min_size)s. "
                  "Your file size is %(size)s."),
    }

    def __init__(self, max_size=None, min_size=None):
        self.max_size = max_size
        self.min_size = min_size

    def __call__(self, data):
        if self.max_size is not None and data.size > self.max_size:
            params = {
                'max_size': filesizeformat(self.max_size),
                'size': filesizeformat(data.size),
            }
            raise ValidationError(self.error_messages['max_size'],
                                   'max_size', params)

        if self.min_size is not None and data.size < self.min_size:
            params = {
                'min_size': filesizeformat(self.min_size),
                'size': filesizeformat(data.size)
            }
            raise ValidationError(self.error_messages['min_size'],
                                   'min_size', params)

    def __eq__(self, other):
        return (
            isinstance(other, FileSizeValidator) and
            self.max_size == other.max_size and
            self.min_size == other.min_size
        )


@deconstructible
class ImageSizeValidator(object):
    error_messages = {
     'max_height': ("Ensure this height size is not greater than %(max_size)s."
                  " Your image height size is %(size)s."),
     'min_height': ("Ensure this height size is not less than %(min_size)s. "
                  "Your image height size is %(size)s."),
     'max_width': ("Ensure this width size is not greater than %(max_size)s."
                  " Your image width size is %(size)s."),
     'min_width': ("Ensure this width size is not less than %(min_size)s. "
                  "Your image width size is %(size)s."),
    }

    def __init__(self, max_height=None, min_height=None, max_width=None, min_width=None):
        self.max_height = max_height
        self.min_height = min_height
        self.max_width = max_width
        self.min_width = min_width

    def __call__(self, data):
        img = Image.open(data)
        fw, fh = img.size

        if self.max_height is not None and fh > self.max_height:
            params = {
                'max_size': str(self.max_height),
                'size': str(fh),
            }
            raise ValidationError(self.error_messages['max_height'],
                                   'max_size', params)

        if self.min_height is not None and fh < self.min_height:
            params = {
                'min_size': str(self.min_width),
                'size': str(fh),
            }
            raise ValidationError(self.error_messages['min_height'],
                                   'min_size', params)

        if self.max_width is not None and fh > self.max_width:
            params = {
                'max_size': str(self.max_width),
                'size': str(fh),
            }
            raise ValidationError(self.error_messages['max_width'],
                                   'max_size', params)

        if self.min_width is not None and fh < self.min_width:
            params = {
                'min_size': str(self.min_width),
                'size': str(fh),
            }
            raise ValidationError(self.error_messages['min_width'],
                                   'min_size', params)

    def __eq__(self, other):
        return (
            isinstance(other, ImageSizeValidator) and
            self.max_height == other.max_height and
            self.min_height == other.min_height and
            self.max_width == other.max_width and
            self.min_width == other.min_width
        )