from django.conf.urls import url, include
from django.conf.urls.static import static
from django.contrib import admin

from i2x_demo import settings

urlpatterns = [
                  url(r'^admin/', admin.site.urls),
                  url(r'^urls/accounts/', include('accounts.urls.urls')),
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
