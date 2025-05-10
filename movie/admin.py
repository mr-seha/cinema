from django.conf import settings
from django.contrib import admin
from django.db.models import Count
from django.urls import reverse
from django.utils.html import format_html
from django.utils.http import urlencode
from jalali_date import datetime2jalali
from jalali_date.admin import ModelAdminJalaliMixin

from .models import Actor, Collection, Comment, Country, Director, Film, Genre, Link


class LinkInline(admin.StackedInline):
    model = Link
    extra = 1


class IMDBRatingFilter(admin.SimpleListFilter):
    title = "امتیاز IMDB"
    parameter_name = "imdb_rating"

    def queryset(self, request, queryset):
        if self.value() == "0_4":
            return queryset.filter(imdb_rating__lt=4)
        elif self.value() == "4_6":
            return queryset.filter(imdb_rating__gte=4, imdb_rating__lt=6)
        elif self.value() == "6_8":
            return queryset.filter(imdb_rating__gte=6, imdb_rating__lt=8)
        elif self.value() == "8_10":
            return queryset.filter(imdb_rating__gte=8)

    def lookups(self, request, model_admin):
        return [
            ("0_4", "کمتر از 4"),
            ("4_6", "بین 4 تا 6"),
            ("6_8", "بین 6 تا 8"),
            ("8_10", "بیشتر از 8"),
        ]


class LinkSizeFilter(admin.SimpleListFilter):
    title = "اندازه"
    parameter_name = "size"

    def lookups(self, request, model_admin):
        return [("0_0.5", "کمتر از ۵۰۰ مگ"),
                ("0.5_1", "بین ۵۰۰ مگ تا ۱ گیگ"),
                ("1_1.5", "بین ۱ گیگ تا ۱.۵ گیگ"),
                ("1.5_2", "بین ۱.۵ گیگ تا ۲ گیگ"),
                ("2_n", "بیش از ۲ گیگ")]

    def queryset(self, request, queryset):
        if self.value() == "0_0.5":
            return queryset.filter(size__lt=500)
        elif self.value() == "0.5_1":
            return queryset.filter(size__gte=500, size__lt=1000)
        elif self.value() == "1_1.5":
            return queryset.filter(size__gte=1000, size__lt=1500)
        elif self.value() == "1.5_2":
            return queryset.filter(size__gte=1500, size__lt=2000)
        elif self.value() == "2_n":
            return queryset.filter(size__gte=2000)


@admin.register(Film)
class FilmAdmin(ModelAdminJalaliMixin, admin.ModelAdmin):
    list_display = [
        "title", "year", "is_serial", "duration_minutes", "visit_count", "imdb_rating_link", "status",
        "created_date_jalali",
        "get_user"]
    list_editable = ["status"]
    readonly_fields = ["user", "visit_count"]
    search_fields = ["title", "title_en"]
    list_filter = ["status", "is_serial", "genres", IMDBRatingFilter, "created_date", "collections", "countries"]
    autocomplete_fields = ["collections", "director", "actors", "countries"]
    inlines = [LinkInline]
    actions = ["make_published"]
    list_select_related = ["user"]
    list_per_page = settings.ADMIN_LIST_PER_PAGE

    @admin.display(description="تاریخ افزودن", ordering="created_date")
    def created_date_jalali(self, film: Film):
        return datetime2jalali(film.created_date).strftime("%d %b %Y %H:%M")

    @admin.display(description="مدت", ordering="duration")
    def duration_minutes(self, film: Film):
        if film.duration:
            return f"{film.duration} دقیقه"
        return "-"

    @admin.display(description="امتیاز imdb", ordering="imdb_rating")
    def imdb_rating_link(self, film: Film):
        return format_html("<a target='_blank' href='{}'>{}</a>", film.imdb_link, film.imdb_rating)

    @admin.display(description="نویسنده", ordering="user")
    def get_user(self, film: Film):
        url = reverse("admin:core_user_changelist") + "?" + urlencode({"id": film.user.id})
        return format_html("<a href='{}'>{}</a>", url, film.user)

    @admin.action(description="منتشر کردن")
    def make_published(self, request, queryset):
        queryset.update(status=Film.STATUS_PUBLISHED)

    def save_model(self, request, obj, form, change):
        obj.user = request.user
        obj.save()


@admin.register(Actor)
class ActorAdmin(admin.ModelAdmin):
    list_display = ["full_name", "full_name_en", "films_count"]
    search_fields = ["full_name", "full_name_en"]
    list_per_page = settings.ADMIN_LIST_PER_PAGE

    @admin.display(description="تعداد فیلم ها")
    def films_count(self, actor: Actor):
        url = reverse("admin:movie_film_changelist") + "?" + \
              urlencode({"actors": actor.id})

        count = Film.objects.filter(actors=actor.id).count()

        if count == 0:
            return 0

        return format_html("<a href='{}'>{}</a>", url, count)


@admin.register(Director)
class DirectorAdmin(admin.ModelAdmin):
    list_display = ["full_name", "full_name_en", "films_count"]
    search_fields = ["full_name", "full_name_en"]
    list_per_page = settings.ADMIN_LIST_PER_PAGE

    @admin.display(description="تعداد فیلم ها")
    def films_count(self, director: Director):
        url = reverse("admin:movie_film_changelist") + "?" + \
              urlencode({"director_id": director.id})

        count = Film.objects.filter(director_id=director.id).count()

        if count == 0:
            return 0

        return format_html("<a href='{}'>{}</a>", url, count)


@admin.register(Collection)
class CollectionAdmin(admin.ModelAdmin):
    list_display = ["title", "count_of_films"]
    search_fields = ["title__istartswith"]
    list_per_page = settings.ADMIN_LIST_PER_PAGE

    def get_queryset(self, request):
        return super().get_queryset(request).annotate(count_of_films=Count("films"))

    @admin.display(description="تعداد فیلم ها")
    def count_of_films(self, collection: Collection):
        url = reverse("admin:movie_film_changelist") + "?" + urlencode({"collections": collection.id})
        count = collection.count_of_films
        if count == 0:
            return 0
        return format_html("<a href='{}'>{}</a>", url, count)


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ["title", "films_count"]
    search_fields = ["title__istartswith"]
    list_per_page = settings.ADMIN_LIST_PER_PAGE

    @admin.display(description="تعداد فیلم ها")
    def films_count(self, genre: Genre):
        url = reverse("admin:movie_film_changelist") + "?" + \
              urlencode({"genres": genre.id})

        count = Film.objects.filter(genres=genre.id).count()

        if count == 0:
            return 0

        return format_html("<a href='{}'>{}</a>", url, count)


@admin.register(Link)
class LinkAdmin(admin.ModelAdmin):
    list_display = ["title", "get_size", "season", "episode", "language", "subtitle", "get_film", "download_link"]
    search_fields = ["film__title", "film__title_en"]
    autocomplete_fields = ["film"]
    list_filter = ["subtitle", "language", "quality", "created_date", LinkSizeFilter]
    list_select_related = ["film"]
    list_per_page = settings.ADMIN_LIST_PER_PAGE

    @admin.display(description="عنوان", ordering="film")
    def title(self, link: Link):
        return f"{link.film.title} {link.film.year} ({link.quality})"

    @admin.display(description="اندازه", ordering="size")
    def get_size(self, link: Link):
        if link.size < 1000:
            return f"{link.size} مگ"
        else:
            return f"{link.size / 1000} گیگ"

    @admin.display(description="دانلود")
    def download_link(self, link: Link):
        return format_html("<a target='_blank' href='{}'>دانلود</a>", link.url)

    @admin.display(description="فیلم مربوطه")
    def get_film(self, link: Link):
        url = reverse("admin:movie_film_changelist") + "?" + urlencode({"id": link.film.id})
        return format_html("<a href='{}'>مشاهده</a>", url)


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ["get_text", "get_user", "status", "rating", "get_film", "created_date"]
    list_display_links = ["get_text"]
    list_editable = ["status"]
    readonly_fields = ["user"]
    search_fields = ["text", "user__first_name", "user__last_name"]
    autocomplete_fields = ["film"]
    list_filter = ["status", "created_date", "rating"]
    list_select_related = ["user", "film"]
    actions = ["make_approved", "make_rejected"]
    list_per_page = settings.ADMIN_LIST_PER_PAGE

    @admin.display(description="کاربر", ordering="user")
    def get_user(self, comment: Comment):
        url = reverse("admin:core_user_changelist") + "?" + urlencode({"id": comment.user.id})
        return format_html("<a href='{}'>{}</a>", url, comment.user)

    @admin.display(description="متن نظر")
    def get_text(self, comment: Comment):
        if len(comment.text) < 20:
            return comment.text
        return comment.text[:20] + "..."

    @admin.display(description="فیلم مربوطه")
    def get_film(self, comment: Comment):
        url = reverse("admin:movie_film_changelist") + "?" + urlencode({"id": comment.film.id})
        return format_html("<a href='{}'>{}</a>", url, comment.film.title)

    @admin.action(description="رد کردن")
    def make_rejected(self, request, queryset):
        queryset.update(status=Comment.STATUS_REJECTED)

    @admin.action(description="تایید کردن")
    def make_approved(self, request, queryset):
        queryset.update(status=Comment.STATUS_APPROVED)

    def save_model(self, request, obj, form, change):
        obj.user = request.user
        obj.save()


@admin.register(Country)
class CountryAdmin(admin.ModelAdmin):
    list_display = ["title", "films_count"]
    search_fields = ["title__istartswith"]
    list_per_page = settings.ADMIN_LIST_PER_PAGE

    @admin.display(description="تعداد فیلم ها")
    def films_count(self, country: Country):
        url = reverse("admin:movie_film_changelist") + "?" + \
              urlencode({"countries": country.id})

        count = Film.objects.filter(countries=country.id).count()

        if count == 0:
            return 0

        return format_html("<a href='{}'>{}</a>", url, count)
