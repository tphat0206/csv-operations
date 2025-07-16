from django.contrib import admin
from django.urls import include
from django.urls import path
from drf_spectacular.views import SpectacularAPIView
from drf_spectacular.views import SpectacularSwaggerView
from rest_framework.routers import SimpleRouter

from account.views.health_check import HealthCheckView


urlpatterns = [
    path('admin/', admin.site.urls),
    path('healthcheck/', HealthCheckView.as_view()),
    path('schema/', SpectacularAPIView.as_view(), name='schema'),
    path('schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/', include('account.urls')),
]

router = SimpleRouter(trailing_slash=True)

urlpatterns += router.urls
