from decimal import Decimal
from django.db import transaction

from apps.payment.models import Wallet


class WalletService:
    """Service class for handling wallet operations."""

    @staticmethod
    def get_or_create_wallet(wallet_id: int) -> Wallet:
        """Get wallet by ID or create if not exists."""
        wallet, created = Wallet.objects.get_or_create(id=wallet_id)
        return wallet

    @staticmethod
    @transaction.atomic
    def add_balance(wallet_id: int, amount: Decimal) -> Wallet:
        """
        Add balance to wallet after successful payment.
        Creates wallet if it doesn't exist.
        Uses select_for_update to prevent race conditions.
        """
        wallet, created = Wallet.objects.select_for_update().get_or_create(
            id=wallet_id,
            defaults={'balance': Decimal('0.00')}
        )
        wallet.balance += amount
        wallet.save(update_fields=['balance', 'updated_at'])
        return wallet

    @staticmethod
    @transaction.atomic
    def deduct_balance(wallet_id: int, amount: Decimal) -> Wallet:
        """
        Deduct balance from wallet after cancelled payment.
        Creates wallet if it doesn't exist (edge case).
        Uses select_for_update to prevent race conditions.
        """
        wallet, created = Wallet.objects.select_for_update().get_or_create(
            id=wallet_id,
            defaults={'balance': Decimal('0.00')}
        )
        wallet.balance -= amount
        wallet.save(update_fields=['balance', 'updated_at'])
        return wallet

