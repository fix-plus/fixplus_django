from django.db import models

from src.authentication.models import User
from src.common.models import BaseModel


class InternalWallet(BaseModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='internal_wallet')
    balance = models.BigIntegerField(default=0)
    frozen_balance = models.BigIntegerField(default=0)
    is_frozen = models.BooleanField(default=False)

    def __str__(self):
        return f"InternalWallet(user={self.user.username}, balance={self.balance})"