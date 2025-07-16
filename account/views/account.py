# Create your views here.
from rest_framework import status, permissions
from rest_framework.decorators import action
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from account.models import Account
from account.serializers.account import SignUpSerializer, CustomTokenObtainPairSerializer, AccountSerializer


class AccountViewSet(GenericViewSet):
    queryset = Account.objects.none()

    def get_serializer_class(self):
        match self.action:
            case 'register':
                return SignUpSerializer
            case 'login':
                return CustomTokenObtainPairSerializer
            case 'me':
                return AccountSerializer

    def get_permissions(self):
        match self.action:
            case 'register' | 'login':
                return [permissions.AllowAny()]
            case 'me':
                return [permissions.IsAuthenticated()]

    @action(methods=['GET'], detail=False)
    def me(self, request: Request):
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)

    @action(methods=['POST'], detail=False)
    def register(self, request: Request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        account = serializer.save()
        return Response({
            "message": "Registration successful",
            "user_id": account.uuid,
        }, status=status.HTTP_201_CREATED)

    @action(methods=['POST'], detail=False)
    def login(self, request: Request):
        serializer = self.get_serializer(data=request.data)
        token = serializer.validate(request.data)
        return Response(token, status=status.HTTP_200_OK)
