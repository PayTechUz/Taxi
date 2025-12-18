from rest_framework import serializers
from django.contrib.auth import get_user_model
from apps.payment.serializers import WalletSerializer
from apps.payment.models import Wallet

User = get_user_model()

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'password', 'first_name', 'last_name']

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        # Create wallet for new user
        Wallet.objects.create(user=user)
        return user

class UserSerializer(serializers.ModelSerializer):
    wallet = WalletSerializer(read_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'wallet']
