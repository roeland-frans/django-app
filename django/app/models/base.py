import uuid

from django.contrib import admin
from django.db import models
from django.utils import timezone


class BaseAdmin(admin.ModelAdmin):
    readonly_fields = ("created", "modified")
    ordering = ("-created",)


class BaseModelManager(models.Manager):
    use_in_migrations = True


class BaseModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created = models.DateTimeField(null=True, default=timezone.now)
    modified = models.DateTimeField(null=True, default=timezone.now)

    class Meta:
        abstract = True
        app_label = "app"

    objects = BaseModelManager()
