from rest_framework.routers import SimpleRouter

from file_service.views import UploadedFileViewSet, CreateFileOperationViewSet, FileOperationStatusViewSet

router = SimpleRouter(trailing_slash=True)
router.register('upload-csv', UploadedFileViewSet)
router.register('perform-operation', CreateFileOperationViewSet, basename='perform-operation')
router.register('task-status', FileOperationStatusViewSet, basename='task-status')

urlpatterns = router.urls
