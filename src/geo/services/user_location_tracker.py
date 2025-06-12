from src.authentication.models import User
from src.geo.models import UserLocationTracker


def create_user_location_tracker(*, user: User, **kwargs):
    return UserLocationTracker.objects.create(user=user, **kwargs)