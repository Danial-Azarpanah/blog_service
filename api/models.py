from django.db import models
from django.utils.html import format_html
from django.utils.text import slugify

from persiantools.jdatetime import JalaliDate

from account.models import User


class Category(models.Model):
    title = models.CharField("عنوان", max_length=30)
    slug = models.SlugField(unique=True, allow_unicode=True,
                            verbose_name="اسلاگ")
    parent = models.ForeignKey("self", verbose_name="دسته بندی مافوق",
                               null=True, blank=True, on_delete=models.SET_NULL,
                               related_name="subs")

    class Meta:
        verbose_name = "دسته بندی"
        verbose_name_plural = "دسته بندی‌ها"

    def __str__(self):
        return self.title


class Post(models.Model):
    title = models.CharField("عنوان", max_length=50)
    slug = models.SlugField(unique=True, allow_unicode=True,
                            verbose_name="اسلاگ",
                            blank=True, null=True)
    category = models.ForeignKey(Category, verbose_name="دسته بندی",
                                 on_delete=models.SET_NULL,
                                 related_name="posts",
                                 null=True, blank=True)
    text = models.TextField("متن مقاله")
    image = models.ImageField(upload_to="media", null=True, blank=True,
                              verbose_name="عکس کاور")
    author = models.ForeignKey(User, on_delete=models.CASCADE,
                               related_name="posts",
                               verbose_name="صاحب محتوا")
    date_created = models.DateTimeField("تاریخ ایجاد", auto_now_add=True)

    class Meta:
        verbose_name = "مقاله"
        verbose_name_plural = "مقالات"

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title, allow_unicode=True)
        super().save()

    def __str__(self):
        return self.title

    # Function to view image of post in admin panel
    def show_image(self):
        return format_html(f'<img src="{self.image.url}" width="60px" height="50px">')
    show_image.short_description = "عکس کاور"

    def jalali_date(self):
        return JalaliDate(self.date_created, locale="fa").strftime("%c")



