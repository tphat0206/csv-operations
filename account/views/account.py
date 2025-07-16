# Create your views here.
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from account.models import Account
from account.serializers.account import SignUpSerializer, SignInSerializer, AccountSerializer


class AccountViewSet(GenericViewSet):
    queryset = Account.objects.none()

    def get_serializer_class(self):
        match self.action:
            case 'sign_up':
                return SignUpSerializer
            case 'sign_in':
                return SignInSerializer
            case 'me':
                return AccountSerializer

    @action(methods=['GET'], detail=False)
    def me(self, request: Request):
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)

    @action(methods=['POST'], detail=False)
    def sign_up(self, request: Request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(methods=['POST'], detail=False)
    def sign_in(self, request: Request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user, token = serializer.sign_in()
        return Response({
            'account': AccountSerializer(user).data,
            'token': token,
        })
