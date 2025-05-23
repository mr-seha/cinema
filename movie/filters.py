from django.contrib.auth import get_user_model
from django_filters import rest_framework as filters

from .models import Film, Link, Comment


class FilmFilter(filters.FilterSet):
    class Meta:
        model = Film
        fields = {
            "status": ["exact"],
            "is_serial": ["exact"],
            "year": ["gte", "lt"],
            "imdb_rating": ["gte", "lt"],
            "genres": ["exact"],
            "collections": ["exact"],
            "countries": ["exact"],
            "original_languages": ["exact"],
            "actors": ["exact"],
            "director": ["exact"],
        }


class LinkFilter(filters.FilterSet):
    quality = filters.ChoiceFilter(choices=Link.QUALITY_CHOICES)
    subtitle = filters.ChoiceFilter(choices=Link.SUBTITLE_CHOICES)
    film = filters.ModelChoiceFilter(queryset=Film.objects.all())

    class Meta:
        model = Link
        fields = {
            "languages": ["exact"],
            "size": ["gte", "lt"],
        }


class CommentFilter(filters.FilterSet):
    rating = filters.ChoiceFilter(choices=[(i, i) for i in range(1, 6)])
    user = filters.ModelChoiceFilter(queryset=get_user_model().objects.all())
    film = filters.ModelChoiceFilter(queryset=Film.objects.all())

    class Meta:
        model = Comment
        fields = {
            "status": ["exact"],
        }
