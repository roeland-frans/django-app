from django.conf import settings
from django.contrib import admin


class AdminSite(admin.AdminSite):
    def each_context(self, request):
        context = super().each_context(request)
        context.update(versions=dict(app=settings.VERSION))
        return context
