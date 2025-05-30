import pytest
from django.contrib.auth import get_user_model
from django.urls import reverse
from model_bakery import baker
from rest_framework import status

from movie import models
from movie.views import FilmViewSet

FILMS_URL = reverse("movie:films-list")


@pytest.fixture
def sample_film_data():
    def get_sample_film_data(**kwargs):
        director = baker.make(models.Director)
        genre = baker.make(models.Genre)
        country = baker.make(models.Country)
        return {
            "title": "گریه ای در شب: افسانه‌ لا یورونا",
            "title_en": "A Cry in the Night: The Legend of La Llorona",
            "year": 2021,
            "description": "description",
            "imdb_rating": 4.0,
            "imdb_link": "https://www.imdb.com/title/tt9001550",
            "director": kwargs.get("director_id", director.id),
            "genres": [kwargs.get("genre_id", genre.id)],
            "countries": [kwargs.get("country_id", country.id)],
        }

    return get_sample_film_data


@pytest.mark.django_db
class TestPrivateFilmAPI:
    def test_create_film_successful(
            self,
            api_client,
            authenticate,
            sample_film_data,
            monkeypatch):
        authenticate(is_staff=True)

        user = baker.make(get_user_model(), is_staff=True)
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

        payload = sample_film_data()
        response = api_client.post(FILMS_URL, payload)

        assert response.status_code == status.HTTP_201_CREATED
        assert response.data["title"] == payload["title"]

    def test_create_film_missing_required_fields(
            self,
            api_client,
            authenticate,
            sample_film_data,
            monkeypatch):
        authenticate(is_staff=True)

        user = baker.make(get_user_model(), is_staff=True)
        monkeypatch.setattr(
            FilmViewSet,
            "get_serializer_context",
            value=lambda _self: {"user": user},
        )

        payload = sample_film_data()

        for key in payload.keys():
            missing_field_payload = payload.copy()
            missing_field_payload.pop(key)

            response = api_client.post(FILMS_URL, missing_field_payload)
            assert response.status_code == status.HTTP_400_BAD_REQUEST
            assert models.Film.objects.count() == 0
