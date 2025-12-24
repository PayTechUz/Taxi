from decimal import Decimal
from django.db import transaction

from paytechuz.gateways.payme import PaymeGateway
from paytechuz.gateways.click import ClickGateway

from apps.payment.models import Wallet

from backend.settings import PAYTECHUZ


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

    @staticmethod
    def create_payment(wallet_id: int, amount: Decimal, provider: str) -> str:
        gateway = None

        if provider == 'payme':
            gateway = PaymeGateway(
                payme_id=PAYTECHUZ.get('PAYME', {}).get('PAYME_ID'),
                payme_key=PAYTECHUZ.get('PAYME', {}).get('PAYME_KEY'),
                is_test_mode=PAYTECHUZ.get('PAYME', {}).get('IS_TEST_MODE'),
            )
            return gateway.create_payment(
                id=wallet_id,
                amount=amount,
            )

        elif provider == 'click':
            gateway = ClickGateway(
                service_id=PAYTECHUZ.get('CLICK', {}).get('SERVICE_ID'),
                merchant_id=PAYTECHUZ.get('CLICK', {}).get('MERCHANT_ID'),
                merchant_user_id=PAYTECHUZ.get('CLICK', {}).get('MERCHANT_USER_ID'),
                secret_key=PAYTECHUZ.get('CLICK', {}).get('SECRET_KEY'),
                is_test_mode=PAYTECHUZ.get('CLICK', {}).get('IS_TEST_MODE'),
            )
            return gateway.create_payment(
                id=wallet_id,
                amount=amount,
            )

        raise ValueError('Invalid provider')

    @staticmethod
    def get_check_data(wallet_id: int) -> dict:
        wallet = Wallet.objects.get(id=wallet_id)
        return {
            "first_name": wallet.user.first_name,
            "amount": float(wallet.balance),
        }

