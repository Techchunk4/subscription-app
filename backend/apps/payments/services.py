import stripe
from django.conf import settings
from users.models import User

stripe.api_key = settings.STRIPE_SECRET_KEY

class StripeService:
    @staticmethod
    def create_customer(user: User):
        customer = stripe.Customer.create(
            email=user.email,
            name=f"{user.first_name} {user.last_name}",
            metadata={
                "user_id": user.id
            }
        )
        return customer

    @staticmethod
    def create_subscription(customer_id, price_id):
        subscription = stripe.Subscription.create(
            customer=customer_id,
            items=[{
                'price': price_id,
            }],
            payment_behavior='default_incomplete',
            expand=['latest_invoice.payment_intent']
        )
        return subscription

    @staticmethod
    def construct_webhook_event(payload, sig_header):
        return stripe.Webhook.construct_event(
            payload, sig_header, settings.STRIPE_WEBHOOK_SECRET
        )