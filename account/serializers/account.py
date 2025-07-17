import logging

from django.db.models import Q
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from account.models import Account

logger = logging.getLogger(__name__)

class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        exclude = ['password']


class NameUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ['uuid', 'first_name', 'last_name']


class SignUpSerializer(serializers.Serializer):
    password = serializers.CharField(write_only=True)
    email = serializers.EmailField()

    def validate_email(self, email):
        if Account.objects.filter(Q(username=email) | Q(email=email)).exists():
            raise serializers.ValidationError('Email existed')
        return email

    def save(self, **kwargs):
        account = Account.objects.create_user(
            self.validated_data.get('email'),
            self.validated_data.get('email'),
            self.validated_data.get('password')
        )
        return account


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    username_field = 'email'
    name = serializers.CharField(read_only=True)
    email = serializers.CharField(read_only=True)

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['username'] = user.username
        token['email'] = user.email
        return token

    def validate(self, attrs):
        data = super().validate(attrs)
        data['user_id'] = self.user.uuid
        data['message'] = 'Login successful!'  # Custom message

        return data

    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        pass
