import logging
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model
from django.db.models import Q

User = get_user_model()
logger = logging.getLogger(__name__)


class EmailOrMobileBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        logger.debug(f"Attempting to authenticate user with username: {username}")

        if username is None:
            username = kwargs.get('email') or kwargs.get('mobile')

        try:
            user = User.objects.get(Q(email=username) | Q(mobile=username))
            logger.debug(f"Found user: {user}")
        except User.DoesNotExist:
            logger.debug("No user found with the provided username")
            return None

        if user.check_password(password) and self.user_can_authenticate(user):
            logger.debug("Password check passed")
            return user
        else:
            logger.debug("Password check failed")
        return None
