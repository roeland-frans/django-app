from app.views.api import ApiView
from app.views.api import GraphiQLView
from django.conf import settings
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
]
