from app.models.base import BaseModel
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.models import UserManager as AuthUserManager
from django.core.mail import send_mail
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from typing import Optional


class UserManager(AuthUserManager):
    def create_user(
        self, email: str, password: Optional[str] = None, **kwargs
    ):
        user = self.model(email=email, **kwargs)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email: str, password: str, **kwargs):
        user = self.model(
            email=email, is_staff=True, is_superuser=True, **kwargs
        )
        user.set_password(password)
        user.save()
        return user


class User(BaseModel, AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(
        _("email address"),
        max_length=255,
        unique=True,
        help_text=_("The user's primary email address."),
    )
    phone_number = models.CharField(
        max_length=30,
        null=True,
        blank=True,
        help_text=_("The user's primary phone number."),
    )
    first_name = models.CharField(
        max_length=250,
        null=True,
        blank=True,
        help_text=_("The user's first name."),
    )
    last_name = models.CharField(
        max_length=250,
        null=True,
        blank=True,
        help_text=_("The user's last name."),
    )
    is_staff = models.BooleanField(
        _("staff status"),
        default=False,
        help_text=_(
            "Designates whether the user can log into this admin site."
        ),
    )
    is_active = models.BooleanField(
        _("active"),
        default=True,
        help_text=_(
            "Designates whether this user should be treated as active. "
            "Unselect this instead of deleting accounts."
        ),
    )
    date_joined = models.DateTimeField(_("date joined"), default=timezone.now)

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = _("User")
        verbose_name_plural = _("Users")
        db_table = "user"
        abstract = False
        app_label = "app"

    def __str__(self):
        return f"{self.email}"

    def clean(self):
        super().clean()
        self.email = self.__class__.objects.normalize_email(self.email)

    def email_user(self, subject, message, from_email=None, **kwargs):
        send_mail(subject, message, from_email, [self.email], **kwargs)

    @property
    def full_name(self) -> str:
        return f"{self.first_name} {self.last_name}".strip()
