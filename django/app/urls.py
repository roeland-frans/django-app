import app.views.errors

from app.views.api import ApiView
from app.views.api import GraphiQLView
from django.conf import settings
from django.conf import urls
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.staticfiles import views
from django.urls import path
from django.urls import re_path
from graphql_jwt.decorators import jwt_cookie

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
    path("graphql/", jwt_cookie(ApiView.as_view()), name="graphql"),
    path(
        "graphiql/",
        GraphiQLView.as_view(graphiql=True),
        name="graphiql",
    ),
    path("400/", lambda request: app.views.errors.error400(request, None)),
    path("403/", lambda request: app.views.errors.error403(request, None)),
    path("404/", lambda request: app.views.errors.error404(request, None)),
    path("500/", app.views.errors.error500),
]

urls.handler400 = "app.views.errors.error400"
urls.handler403 = "app.views.errors.error403"
urls.handler404 = "app.views.errors.error404"
urls.handler500 = "app.views.errors.error500"
