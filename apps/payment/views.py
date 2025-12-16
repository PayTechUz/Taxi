from paytechuz.integrations.django.views import BasePaymeWebhookView, BaseClickWebhookView

from apps.payment.services import WalletService


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

