from datetime import datetime

from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from .validators import film_thumbnail_size_validator


class Genre(models.Model):
    title = models.CharField(max_length=255, verbose_name="عنوان")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "ژانر"
        verbose_name_plural = "ژانر"


class Collection(models.Model):
    title = models.CharField(max_length=255, verbose_name="عنوان")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "دسته بندی"
        verbose_name_plural = "دسته بندی"


class Director(models.Model):
    full_name = models.CharField(
        max_length=255,
        verbose_name="نام و نام خانوادگی"
    )
    full_name_en = models.CharField(
        max_length=255,
        verbose_name="نام و نام خانوادگی انگلیسی"
    )
    picture = models.ImageField(
        upload_to="movie/images",
        null=True,
        blank=True,
        verbose_name="تصویر"
    )

    def __str__(self):
        return self.full_name

    class Meta:
        verbose_name = "کارگردان"
        verbose_name_plural = "کارگردان"


class Actor(models.Model):
    full_name = models.CharField(
        max_length=255,
        verbose_name="نام و نام خانوادگی"
    )
    full_name_en = models.CharField(
        max_length=255,
        verbose_name="نام و نام خانوادگی انگلیسی"
    )
    picture = models.ImageField(
        upload_to="movie/images",
        null=True,
        blank=True,
        verbose_name="تصویر"
    )

    def __str__(self):
        return self.full_name

    class Meta:
        verbose_name = "بازیگر"
        verbose_name_plural = "بازیگر"


class Country(models.Model):
    title = models.CharField(max_length=255, verbose_name="نام کشور")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "کشور"
        verbose_name_plural = "کشور"


class Language(models.Model):
    title = models.CharField(max_length=255, verbose_name="نام")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "زبان"
        verbose_name_plural = "زبان"


class Film(models.Model):
    STATUS_DRAFT = "D"
    STATUS_PUBLISHED = "P"

    STATUS_CHOICES = [
        (STATUS_DRAFT, "پیش نویس"),
        (STATUS_PUBLISHED, "منتشر شده"),
    ]
    title = models.CharField(max_length=255, verbose_name="عنوان")
    title_en = models.CharField(max_length=255, verbose_name="عنوان انگلیسی")

    year = models.PositiveSmallIntegerField(
        validators=[
            MinValueValidator(1700),
            MaxValueValidator(datetime.now().year)
        ],
        verbose_name="سال تولید(میلادی)",
    )
    description = models.TextField(verbose_name="توضیح")
    thumbnail = models.ImageField(
        upload_to="movie/images",
        validators=[film_thumbnail_size_validator],
        null=True,
        blank=True,
        verbose_name="تصویر"
    )
    status = models.CharField(
        max_length=1,
        choices=STATUS_CHOICES,
        default=STATUS_PUBLISHED,
        verbose_name="وضعیت انتشار"
    )
    imdb_rating = models.FloatField(
        validators=[MinValueValidator(0), MaxValueValidator(10)],
        verbose_name="امتیاز imdb",
    )
    imdb_link = models.URLField(max_length=255, verbose_name="لینک imdb")

    countries = models.ManyToManyField(
        Country,
        related_name="films",
        blank=False,
        verbose_name="کشور ها"
    )

    original_languages = models.ManyToManyField(
        Language,
        related_name="films",
        blank=False,
        verbose_name="زبان ها"
    )

    duration = models.PositiveSmallIntegerField(
        null=True,
        blank=True,
        verbose_name="مدت(دقیقه)"
    )
    created_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name="تاریخ افزودن فیلم"
    )

    last_update_date = models.DateTimeField(
        auto_now=True,
        verbose_name="تاریخ آخرین ویرایش"
    )
    is_serial = models.BooleanField(default=False, verbose_name="سریال؟")

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="films",
        verbose_name="کاربر"
    )

    director = models.ForeignKey(
        Director,
        on_delete=models.PROTECT,
        related_name="films",
        verbose_name="کارگردان"
    )

    actors = models.ManyToManyField(
        Actor,
        related_name="films",
        blank=True,
        verbose_name="بازیگر ها"
    )

    collections = models.ManyToManyField(
        Collection,
        related_name="films",
        blank=True,
        verbose_name="دسته بندی ها"
    )

    genres = models.ManyToManyField(
        Genre,
        related_name="films",
        blank=False,
        verbose_name="ژانر ها"
    )

    visit_count = models.PositiveIntegerField(
        default=0,
        verbose_name="تعداد بازدید"
    )

    def __str__(self):
        return f"{self.title}({self.year})"

    class Meta:
        verbose_name = "فیلم"
        verbose_name_plural = "فیلم"


class Link(models.Model):
    QUALITY_360P = "360P"
    QUALITY_480P = "480P"
    QUALITY_720P = "720P"
    QUALITY_1080P = "1080P"
    QUALITY_2K = "2K"
    QUALITY_4K = "4K"
    QUALITY_CHOICES = [
        (QUALITY_360P, "360P"),
        (QUALITY_480P, "480P"),
        (QUALITY_720P, "720P"),
        (QUALITY_1080P, "1080P"),
        (QUALITY_2K, "2K"),
        (QUALITY_4K, "4K"),
    ]

    SUBTITLE_NO_SUB = "NS"
    SUBTITLE_PERSIAN_HARD_SUB = "PHS"
    SUBTITLE_ENGLISH_HARD_SUB = "EHS"
    SUBTITLE_CHOICES = [
        (SUBTITLE_NO_SUB, "ندارد"),
        (SUBTITLE_PERSIAN_HARD_SUB, "زیرنویسی فارسی چسبیده"),
        (SUBTITLE_ENGLISH_HARD_SUB, "زیرنویس انگلیسی چسبیده"),
    ]

    url = models.URLField(max_length=255, verbose_name="آدرس")
    size = models.PositiveSmallIntegerField(verbose_name="اندازه(مگابایت)")

    languages = models.ManyToManyField(
        Language,
        related_name="links",
        blank=False,
        verbose_name="زبان ها"
    )

    subtitle = models.CharField(
        max_length=255,
        choices=SUBTITLE_CHOICES,
        default=SUBTITLE_NO_SUB,
        verbose_name="زیرنویس"
    )

    quality = models.CharField(
        max_length=255,
        choices=QUALITY_CHOICES,
        default=QUALITY_720P,
        verbose_name="کیفیت"
    )

    season = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1)],
        null=True,
        blank=True,
        verbose_name="فصل"
    )
    episode = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1)],
        null=True,
        blank=True,
        verbose_name="قسمت"
    )

    created_date = models.DateTimeField(
        auto_now_add=True, verbose_name="تاریخ افزودن"
    )

    film = models.ForeignKey(
        Film,
        on_delete=models.CASCADE,
        related_name="links",
        verbose_name="فیلم"
    )

    def __str__(self):
        return f"{self.film.title} ({self.quality})"

    class Meta:
        verbose_name = "لینک"
        verbose_name_plural = "لینک"


class Comment(models.Model):
    STATUS_PENDING = "P"
    STATUS_APPROVED = "A"
    STATUS_REJECTED = "R"

    STATUS_CHOICES = [
        (STATUS_PENDING, "در انتظار تایید"),
        (STATUS_APPROVED, "تایید شده"),
        (STATUS_REJECTED, "تایید نشده"),
    ]

    text = models.TextField(verbose_name="نظر")
    rating = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        null=True,
        blank=True,
        verbose_name="امتیاز به فیلم",
    )
    like_count = models.PositiveSmallIntegerField(
        default=0,
        verbose_name="لایک ها"
    )
    dislike_count = models.PositiveSmallIntegerField(
        default=0, verbose_name="دیسلایک ها"
    )

    status = models.CharField(
        max_length=1,
        choices=STATUS_CHOICES,
        default=STATUS_PENDING,
        verbose_name="وضعیت تایید"
    )

    created_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name="تاریخ"
    )

    film = models.ForeignKey(
        Film,
        on_delete=models.CASCADE,
        related_name="comments",
        verbose_name="فیلم مربوطه"
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="comments",
        verbose_name="کاربر"
    )

    parent = models.ForeignKey(
        "self",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        verbose_name="والد"
    )

    def __str__(self):
        max_text_length = 25
        if len(self.text) < max_text_length:
            return self.text
        return self.text[:max_text_length] + " ..."

    class Meta:
        verbose_name = "نظر"
        verbose_name_plural = "نظر"
