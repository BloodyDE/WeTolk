from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("", include(("tickets.urls", "tickets"), namespace="tickets")),   # alles der Tickets-App am Root
    path("convert/", include(("WeConvert.urls", "weconvert"), namespace="weconvert")),
    path("admin/", admin.site.urls),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)