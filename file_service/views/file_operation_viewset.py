import django_filters
from django_filters import rest_framework as filters
from rest_framework import viewsets, mixins, permissions

from file_service.models import FileOperation
from file_service.serializers import CreateFileOperationSerializer
from file_service.serializers.file_operation import FileOperationSerializer


class FileOperationFilter(filters.FilterSet):
    uuid = django_filters.CharFilter(field_name='uuid')

    def __init__(self, *args, **kwargs):
        self.n_param = kwargs['data'].get('n', None)
        super().__init__(*args, **kwargs)
        if self.request and self.n_param is not None:
            self.request.n_value = int(self.n_param)

    class Meta:
        model = FileOperation
        fields = [
            'uuid',
        ]


class CreateFileOperationViewSet(
    viewsets.GenericViewSet,
    mixins.CreateModelMixin,
):
    queryset = FileOperation.objects.all()
    serializer_class = CreateFileOperationSerializer
    permission_classes = [permissions.IsAuthenticated]
    filterset_class = FileOperationFilter



class FileOperationStatusViewSet(
    viewsets.GenericViewSet,
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin
):
    queryset = FileOperation.objects.all()
    serializer_class = FileOperationSerializer
    permission_classes = [permissions.IsAuthenticated]
    filterset_class = FileOperationFilter