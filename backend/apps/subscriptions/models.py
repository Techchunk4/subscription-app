from django.db import models
from users.models import User

class Plan(models.Model):
    name = models.CharField(max_length=100)
    stripe_price_id = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    interval = models.CharField(max_length=10, choices=[('month', 'Monthly'), ('year', 'Yearly')])
    features = models.JSONField(default=list)

    def __str__(self):
        return self.name

class UserSubscription(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    plan = models.ForeignKey(Plan, on_delete=models.SET_NULL, null=True)
    stripe_subscription_id = models.CharField(max_length=255)
    status = models.CharField(max_length=20)
    current_period_end = models.DateTimeField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.email} - {self.plan.name}"