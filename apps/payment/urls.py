from django.urls import path
from .views import PaymeWebhookView, ClickWebhookView

urlpatterns = [
    path('payme/webhook/', PaymeWebhookView.as_view(), name='payme_webhook'),
    path('click/webhook/', ClickWebhookView.as_view(), name='click_webhook'),
]
