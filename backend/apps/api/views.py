from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from subscriptions.models import Plan
from subscriptions.serializers import PlanSerializer
from payments.services import StripeService

class PlanViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Plan.objects.all()
    serializer_class = PlanSerializer

    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def subscribe(self, request, pk=None):
        plan = self.get_object()
        user = request.user
        
        if not user.stripe_customer_id:
            customer = StripeService.create_customer(user)
            user.stripe_customer_id = customer.id
            user.save()
        
        subscription = StripeService.create_subscription(
            user.stripe_customer_id,
            plan.stripe_price_id
        )
        
        return Response({
            'client_secret': subscription.latest_invoice.payment_intent.client_secret,
            'subscription_id': subscription.id
        }, status=status.HTTP_200_OK)