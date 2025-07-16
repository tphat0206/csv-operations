from drf_spectacular.utils import extend_schema
from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from file_service.models import UploadedFile
from file_service.serializers import UploadedFileSerializer

class UploadedFileViewSet(viewsets.ModelViewSet):
    queryset = UploadedFile.objects.all()
    serializer_class = UploadedFileSerializer
    permission_classes = [IsAuthenticated]


    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.uploaded_by != self.request.user:
            return Response(
                {'error': 'You do not have permission to delete this file.'},
                status=status.HTTP_403_FORBIDDEN
            )
        super(UploadedFileViewSet, self).destroy(request, *args, **kwargs)
        return Response(status=status.HTTP_204_NO_CONTENT)

    @extend_schema(methods=['PUT'], exclude=True)
    def update(self, request, *args, **kwargs):
        pass

    @extend_schema(methods=['PATCH'], exclude=True)
    def partial_update(self, request, *args, **kwargs):
        pass