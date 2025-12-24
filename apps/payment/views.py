from rest_framework.views import APIView
from rest_framework.response import Response

from paytechuz.integrations.django.views import BasePaymeWebhookView, BaseClickWebhookView

from rest_framework import permissions
from apps.payment.models import Wallet
from apps.payment.services import WalletService


class TopUpBalanceView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        """Create payment."""
        amount = request.data.get('amount')
        provider = request.data.get('provider')

        if not amount or not provider:
            return Response({'error': 'Missing required fields'}, status=400)

        wallet, _ = Wallet.objects.get_or_create(user=request.user)

        payment_url = WalletService.create_payment(wallet.id, amount, provider)

        return Response({'payment_url': payment_url})


class PaymeWebhookView(BasePaymeWebhookView):
    def successfully_payment(self, params, transaction):
        """Handle successful Payme payment."""
        WalletService.add_balance(
            wallet_id=transaction.account_id,
            amount=transaction.amount
        )

    def cancelled_payment(self, params, transaction):
        """Handle cancelled Payme payment."""
        WalletService.deduct_balance(
            wallet_id=transaction.account_id,
            amount=transaction.amount
        )

    def get_check_data(self, params, account):
        """
        Additional data to check transaction.
        This method is optional.
        """
        check_info = WalletService.get_check_data(account.id)
        return {
            "additional": check_info
        }


class ClickWebhookView(BaseClickWebhookView):
    def successfully_payment(self, params, transaction):
        """Handle successful Click payment."""
        WalletService.add_balance(
            wallet_id=transaction.account_id,
            amount=transaction.amount
        )

    def cancelled_payment(self, params, transaction):
        """Handle cancelled Click payment."""
        WalletService.deduct_balance(
            wallet_id=transaction.account_id,
            amount=transaction.amount
        )

