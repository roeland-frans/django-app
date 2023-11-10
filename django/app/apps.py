from django import apps
from django.contrib.admin import site
from django.contrib.admin.apps import AdminConfig


class AppAdminConfig(AdminConfig):
    default_site = "app.admin.site.AdminSite"


class AppConfig(apps.AppConfig):
    name = "app"
    label = "app"

    def ready(self):
        # Register Django models here
        from app.admin.user import UserAdmin
        from app.models.user import User

        site.register(User, UserAdmin)
