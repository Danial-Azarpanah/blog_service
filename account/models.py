from django.db import models
from django.contrib.auth.models import AbstractBaseUser

from persiantools.jdatetime import JalaliDate

from .managers import UserManager


class User(AbstractBaseUser):
    phone_number = models.CharField("شماره موبایل", max_length=11, unique=True)
    full_name = models.CharField("نام و نام خانوادگی", max_length=50)
    date_joined = models.DateTimeField("تاریخ عضویت", auto_now_add=True)
    is_admin = models.BooleanField("دسترسی ادمین", default=False)
    is_active = models.BooleanField("حساب فعال است", default=False)

    objects = UserManager()

    USERNAME_FIELD = "phone_number"
    REQUIRED_FIELDS = ("full_name",)

    class Meta:
        verbose_name = "کاربر"
        verbose_name_plural = "کاربرها"

    def __str__(self):
        return f"{self.full_name} - {self.phone_number[-4:]}"

    def jalali_date(self):
        return JalaliDate(self.date_joined, locale="fa").strftime("%c")
    jalali_date.short_description = "تاریخ عضویت"

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_admin



