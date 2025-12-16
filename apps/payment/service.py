from decimal import Decimal
from typing import Optional
from .models import Wallet


class PaymentGatewayService:
    def process_payment(self, amount: Decimal, token: str) -> bool:
        """Process a payment from an external source."""
        raise NotImplementedError

    def refund_payment(self, transaction_id: str) -> bool:
        """Refund a previous payment."""
        raise NotImplementedError


class WalletService:
    def create_wallet(self, user) -> Wallet:
        """Create a wallet for a user."""
        return Wallet.objects.create(user=user)

    def get_wallet(self, user) -> Optional[Wallet]:
        """Retrieve a user's wallet."""
        return getattr(user, 'wallet', None)

    def deposit(self, wallet: Wallet, amount: Decimal) -> Wallet:
        """Add funds to the wallet."""
        wallet.balance += amount
        wallet.save()
        return wallet
    
    def withdraw(self, wallet: Wallet, amount: Decimal) -> Wallet:
        """Subtract funds from the wallet."""
        if wallet.balance < amount:
            raise ValueError("Insufficient funds")
        wallet.balance -= amount
        wallet.save()
        return wallet

    def get_balance(self, wallet: Wallet) -> Decimal:
        """Get current balance."""
        return wallet.balance
