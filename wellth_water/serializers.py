from rest_framework import serializers
from .models import Users
from .models import Entries
from .models import Transactions


class UsersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = ("name", "email")

class EntriesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Entries
        fields = ("type", "amount")

class UserEntriesSerializer(serializers.Serializer):
     entries = EntriesSerializer(many=True)

class TransactionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transactions
        fields = ("amount",)
