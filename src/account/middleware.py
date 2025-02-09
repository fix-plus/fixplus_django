from django.utils import timezone
from django.contrib.auth import get_user_model
from django.utils.deprecation import MiddlewareMixin
from rest_framework_simplejwt.tokens import AccessToken


class UpdateLastOnlineMiddleware(MiddlewareMixin):
    def process_request(self, request):
        if request.user.is_authenticated:
            self._update_last_online(request.user)
        else:
            # Attempt to retrieve account from HTTP headers (optional)
            authorization = request.META.get('HTTP_AUTHORIZATION')
            if authorization and authorization.startswith('Bearer '):
                token = authorization.split()[1]  # Extract token
                try:
                    user = self._get_user_from_token(token)
                    if user:
                        self._update_last_online(user)
                except Exception as e:
                    print(f"Error retrieving account from token: {e}")

        return None  # Return None to continue processing the request

    def _update_last_online(self, user):
        """
        Updates account's last_online field and saves the account.
        """

        user.last_online = timezone.now()
        user.save(update_fields=['last_online'])

    def _get_user_from_token(self, token):
        try:
            access_token = AccessToken(token)
            user_id = access_token['user_id']
            User = get_user_model()
            user = User.objects.get(pk=user_id)
            return user
        except (ValueError, KeyError, User.DoesNotExist):
            return None