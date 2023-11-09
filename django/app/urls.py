from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.urls import re_path
from django.contrib.staticfiles import views
from django.conf.urls.static import static

urlpatterns = []

if settings.DEBUG:
    urlpatterns += [
        re_path(r"^static/(?P<path>.*)$", views.serve),
    ]
    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT
    )

urlpatterns += [
    path("admin/", admin.site.urls),
]
