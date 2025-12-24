from django.urls import path

from apps.payment.views import PaymeWebhookView, ClickWebhookView, TopUpBalanceView, UzumWebhookView


urlpatterns = [
    path('top-up/', TopUpBalanceView.as_view(), name='top_up_balance'),
    path('payme/webhook/', PaymeWebhookView.as_view(), name='payme_webhook'),
    path('click/webhook/', ClickWebhookView.as_view(), name='click_webhook'),
    path('uzum/webhook/<str:action>', UzumWebhookView.as_view(), name='uzum_webhook'),
]
