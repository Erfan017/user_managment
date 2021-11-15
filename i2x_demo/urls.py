from django.conf.urls import url, include
from django.conf.urls.static import static
from django.contrib import admin

from i2x_demo import settings
from django.conf.urls import url
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions

schema_view = get_schema_view(
    openapi.Info(
        title="Bina admin API",
        default_version='v1',
        description="Bina admin API",
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)
urlpatterns = [
                  url(r'^docs/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
                  url(r'^admin/', admin.site.urls),
                  url(r'^urls/accounts/', include('accounts.urls.urls')),
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
