from rest_framework import serializers

from .models import Account


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = Account
        fields = ['id', 'email', 'first_name', 'last_name']