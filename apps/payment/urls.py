from django.urls import path

from apps.payment.views import PaymeWebhookView, ClickWebhookView, TopUpBalanceView


urlpatterns = [
    path('top-up/', TopUpBalanceView.as_view(), name='top_up_balance'),
    path('payme/webhook/', PaymeWebhookView.as_view(), name='payme_webhook'),
    path('click/webhook/', ClickWebhookView.as_view(), name='click_webhook'),
]
