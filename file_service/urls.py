from rest_framework.routers import SimpleRouter

from file_service.views import UploadedFileViewSet, FileOperationViewSet

router = SimpleRouter(trailing_slash=True)
router.register('upload-csv', UploadedFileViewSet)
router.register('perform-operation', FileOperationViewSet)

urlpatterns = router.urls
