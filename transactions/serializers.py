from .models        import Transaction, Account
from rest_framework import serializers

class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = ('__all__')

class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ('number',)        

class AccountDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ('account', 'balance', 'owner', 'created_date')

class TransactionListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = ('fromaccount', 'toaccount', 'amount', 'created_date', )        

