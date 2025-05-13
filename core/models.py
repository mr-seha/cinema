from django.contrib.auth.models import AbstractUser
from django.db import models
from solo.models import SingletonModel


class User(AbstractUser):
    email = models.EmailField(unique=True, max_length=255, verbose_name="ایمیل")

    def __str__(self):
        display_name = ""
        if self.first_name:
            display_name += self.first_name

        if self.last_name:
            if display_name:
                display_name += " "
            display_name += self.last_name

        if not display_name:
            display_name += self.username
        return display_name


class SiteConfiguration(SingletonModel):
    site_title = models.CharField(max_length=255, default="دانلود فیلم", verbose_name="عنوان سایت")

    def __str__(self):
        return "تنظیمات سایت"

    class Meta:
        verbose_name = "تنظیمات سایت"
