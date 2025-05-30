import pytest
from django.contrib.auth import get_user_model
from django.urls import reverse
from model_bakery import baker
from rest_framework import status

from movie import models
from movie.views import FilmViewSet

FILMS_URL = reverse("movie:films-list")


@pytest.mark.django_db
class TestPrivateFilmAPI:
    def test_create_film_successful(
            self,
            api_client,
            authenticate,
            monkeypatch):
        authenticate(is_staff=True)

        user = baker.make(get_user_model(), is_staff=True)
        director = baker.make(models.Director)
        genre = baker.make(models.Genre)
        country = baker.make(models.Country)
        language = baker.make(models.Language)

        monkeypatch.setattr(
            FilmViewSet,
            "get_serializer_context",
            value=lambda _self: {"user": user},
        )

        # If we decide to use mocker instead of monkeypatch:
        # mocker.patch(
        #     "movie.views.FilmViewSet.get_serializer_context",
        #     return_value={"user": user}
        # )

        payload = {
            "title": "گریه ای در شب: افسانه‌ لا یورونا",
            "title_en": "A Cry in the Night: The Legend of La Llorona",
            "year": 2021,
            "description": "description",
            "imdb_rating": 4.0,
            "imdb_link": "https://www.imdb.com/title/tt9001550",
            "genres": [genre.id],
            "director": director.id,
            "countries": [country.id],
            "original_languages": [language.id],
        }

        response = api_client.post(FILMS_URL, payload)
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data["title"] == payload["title"]
