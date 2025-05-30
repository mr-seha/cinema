# Generated by Django 5.1.4 on 2024-12-18 07:51

import django.core.validators
import django.db.models.deletion
import movie.validators
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Character',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('full_name', models.CharField(max_length=255, verbose_name='نام و نام خانوادگی')),
                ('full_name_en', models.CharField(max_length=255, verbose_name='نام و نام خانوادگی انگلیسی')),
                ('picture', models.ImageField(blank=True, null=True, upload_to='movie/images', verbose_name='تصویر')),
            ],
            options={
                'verbose_name': 'شخصیت',
                'verbose_name_plural': 'شخصیت',
            },
        ),
        migrations.CreateModel(
            name='Collection',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255, verbose_name='عنوان')),
            ],
            options={
                'verbose_name': 'دسته بندی',
                'verbose_name_plural': 'دسته بندی',
            },
        ),
        migrations.CreateModel(
            name='Film',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255, verbose_name='عنوان')),
                ('title_en', models.CharField(max_length=255, verbose_name='عنوان انگلیسی')),
                ('description', models.TextField(verbose_name='توضیح')),
                ('thumbnail', models.ImageField(blank=True, null=True, upload_to='movie/images',
                                                validators=[movie.validators.film_thumbnail_size_validator],
                                                verbose_name='تصویر')),
                ('status', models.CharField(choices=[('D', 'پیش نویس'), ('P', 'منتشر شده')], default='P', max_length=1,
                                            verbose_name='وضعیت انتشار')),
                ('imdb_rating', models.FloatField(validators=[django.core.validators.MinValueValidator(0),
                                                              django.core.validators.MaxValueValidator(10)],
                                                  verbose_name='امتیاز imdb')),
                ('imdb_link', models.URLField(max_length=255, verbose_name='لینک imdb')),
                ('year', models.PositiveSmallIntegerField(validators=[django.core.validators.MinValueValidator(1700),
                                                                      django.core.validators.MaxValueValidator(2024)],
                                                          verbose_name='سال تولید(میلادی)')),
                ('country', models.CharField(max_length=255, verbose_name='کشور سازنده')),
                ('duration', models.PositiveSmallIntegerField(blank=True, null=True, verbose_name='مدت(دقیقه)')),
                ('created_date', models.DateTimeField(auto_now_add=True, verbose_name='تاریخ افزودن فیلم')),
                ('last_update_date', models.DateTimeField(auto_now=True, verbose_name='تاریخ آخرین ویرایش')),
                ('is_serial', models.BooleanField(default=False, verbose_name='سریال؟')),
                ('collections',
                 models.ManyToManyField(related_name='films', to='movie.collection', verbose_name='دسته بندی ها')),
                ('director',
                 models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='director_films',
                                   to='movie.character', verbose_name='کارگردان')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL,
                                           verbose_name='کاربر')),
            ],
            options={
                'verbose_name': 'فیلم',
                'verbose_name_plural': 'فیلم',
            },
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField(verbose_name='نظر')),
                ('rating', models.PositiveSmallIntegerField(validators=[django.core.validators.MinValueValidator(1),
                                                                        django.core.validators.MaxValueValidator(5)],
                                                            verbose_name='امتیاز به فیلم')),
                ('like_count', models.PositiveSmallIntegerField(default=0, verbose_name='لایک ها')),
                ('dislike_count', models.PositiveSmallIntegerField(default=0, verbose_name='دیسلایک ها')),
                ('status', models.CharField(choices=[('P', 'در انتظار تایید'), ('A', 'تایید شده'), ('R', 'تایید نشده')],
                                            default='P', max_length=1, verbose_name='وضعیت تایید')),
                ('created_date', models.DateTimeField(auto_now_add=True, verbose_name='تاریخ')),
                ('user',
                 models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL,
                                   verbose_name='کاربر')),
                ('film', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='movie.film',
                                           verbose_name='فیلم مربوطه')),
            ],
            options={
                'verbose_name': 'نظر',
                'verbose_name_plural': 'نظر',
            },
        ),
        migrations.CreateModel(
            name='Link',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('url', models.URLField(max_length=255, verbose_name='آدرس')),
                ('size', models.PositiveSmallIntegerField(verbose_name='اندازه(مگابایت)')),
                ('language', models.CharField(default='فارسی', max_length=255, verbose_name='زبان')),
                ('subtitle', models.CharField(
                    choices=[('NS', 'ندارد'), ('PHS', 'زیرنویسی فارسی چسبیده'), ('EHS', 'زیرنویس انگلیسی چسبیده')],
                    default='NS', max_length=255, verbose_name='زیرنویس')),
                ('quality', models.CharField(
                    choices=[('360P', '360P'), ('480P', '480P'), ('720P', '720P'), ('1080P', '1080P'), ('2K', '2K'),
                             ('4K', '4K')], default='720P', max_length=255, verbose_name='کیفیت')),
                ('season', models.PositiveSmallIntegerField(blank=True, null=True,
                                                            validators=[django.core.validators.MinValueValidator(1)],
                                                            verbose_name='فصل')),
                ('episode', models.PositiveSmallIntegerField(blank=True, null=True,
                                                             validators=[django.core.validators.MinValueValidator(1)],
                                                             verbose_name='قسمت')),
                ('film',
                 models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='links', to='movie.film',
                                   verbose_name='فیلم')),
            ],
            options={
                'verbose_name': 'لینک',
                'verbose_name_plural': 'لینک',
            },
        ),
        migrations.CreateModel(
            name='CharacterItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('character', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='movie.character',
                                                verbose_name='شخصیت')),
                ('film',
                 models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='movie.film', verbose_name='فیلم')),
            ],
            options={
                'verbose_name': 'شخصیت',
                'verbose_name_plural': 'شخصیت',
                'unique_together': {('character', 'film')},
            },
        ),
    ]
