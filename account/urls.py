from rest_framework.routers import SimpleRouter

from account.views.account import AccountViewSet
from django.urls import path

from rest_framework_simplejwt.views import (
    TokenRefreshView,
)

router = SimpleRouter(trailing_slash=True)
urlpatterns = [
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
router.register('', AccountViewSet)

urlpatterns += router.urls