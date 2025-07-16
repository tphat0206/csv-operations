from django.contrib.auth import authenticate
from rest_framework import serializers
from rest_framework.authtoken.models import Token
from rest_framework.exceptions import AuthenticationFailed

from account.models import Account

class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        exclude = ['password']

class NameUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ['uuid', 'first_name', 'last_name']


class SignUpSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)
    email = serializers.EmailField()
    first_name = serializers.CharField()
    last_name = serializers.CharField()

    def validate_username(self, username):
        if Account.objects.filter(username=username).exists():
            raise serializers.ValidationError('username existed')
        return username

    def save(self, **kwargs):
        Account.objects.create_user(
            self.validated_data.get('username'),
            self.validated_data.get('email'),
            self.validated_data.get('password')
        ).update(first_name=self.validated_data.get('first_name'),last_name=self.validated_data.get('last_name'))


class SignInSerializer(serializers.Serializer):
    username = serializers.CharField(write_only=True)
    password = serializers.CharField(write_only=True)

    token = serializers.CharField(read_only=True)

    def sign_in(self):
        username = self.validated_data.get('username')
        password = self.validated_data.get('password')

        user = authenticate(request=self.context.get('request'),
                            username=username, password=password)
        if not user:
            raise AuthenticationFailed

        token, created = Token.objects.get_or_create(user=user)
        return user, token.key
