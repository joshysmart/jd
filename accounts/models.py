from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from django.utils.timezone import now


class CustomUser(AbstractUser):
    email = models.EmailField(_('email address'), unique=True)
    dob = models.DateField(_("Date"), default=now)
    gender = models.CharField(max_length=7, default="")
    profile_completed = models.BooleanField(default=False)


class Profile(models.Model):
    username = models.CharField(max_length=256, unique=True)
    dob = models.DateField(_("Date"), default=now)
    gender = models.CharField(max_length=7, default="")
    profile_completed = models.BooleanField(default=False)
    user = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE,  related_name="profiles")
