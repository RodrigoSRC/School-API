from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .models import Account


class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ["id", "username", "email", "password", "is_superuser"]
        extra_kwargs = {
            "password": {"write_only": True},
        }

    class CustomJWTSerializer(TokenObtainPairSerializer):
        @classmethod
        def get_token(cls, user):
            token = super().get_token(user)
            token["is_superuser"] = user.is_superuser
            return token
