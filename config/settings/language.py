import os
from django.utils.translation import gettext_lazy as _

from config.env import BASE_DIR

# Base language code
LANGUAGE_CODE = 'en'

# Enable Django’s translation system
USE_I18N = True

# Enable localization of data
USE_L10N = True

# Enable timezone support
USE_TZ = True

# Define the supported languages
LANGUAGES = [
    ('en', _('English')),
    ('fa', _('Persian')),  # Persian (Farsi)
]

# Path to locale files
LOCALE_PATHS = [
    os.path.join(BASE_DIR, 'locale'),
]