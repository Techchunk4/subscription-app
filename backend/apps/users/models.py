from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    stripe_customer_id = models.CharField(max_length=255, blank=True, null=True)
    subscription_active = models.BooleanField(default=False)
    
    def __str__(self):
        return self.email