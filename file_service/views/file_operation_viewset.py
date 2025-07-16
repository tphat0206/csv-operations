from rest_framework import viewsets, mixins, permissions

from file_service.models import FileOperation
from file_service.serializers import FileOperationSerializer


class FileOperationViewSet(
    viewsets.GenericViewSet,
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin
):
    queryset = FileOperation.objects.all()
    serializer_class = FileOperationSerializer
    permission_classes = [permissions.IsAuthenticated]
