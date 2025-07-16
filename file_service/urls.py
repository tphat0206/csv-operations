from rest_framework.routers import SimpleRouter

from file_service.views import UploadedFileViewSet

router = SimpleRouter(trailing_slash=True)
router.register('upload-csv', UploadedFileViewSet)

urlpatterns = router.urls
