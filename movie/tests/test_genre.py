import pytest
from django.urls import reverse
from model_bakery import baker
from rest_framework import status

from movie.models import Genre
from movie.serializers import GenreSerializer

GENRES_URL = reverse("movie:genre-list")


def genre_url(genre_id):
    return reverse("movie:genre-detail", args=[genre_id])


@pytest.mark.django_db
class TestPublicGenreAPI:
    def test_retrieve_genres(self, api_client):
        response = api_client.get(GENRES_URL)
        assert response.status_code == status.HTTP_200_OK

    def test_retrieve_genre(self, api_client):
        genre = baker.make(Genre)

        response = api_client.get(genre_url(genre.id))
        assert response.status_code == status.HTTP_200_OK

        serializer = GenreSerializer(genre)
        assert serializer.data == response.data


@pytest.mark.django_db
class TestPrivateGenreAPI:
    def test_user_is_not_admin(self, api_client, authenticate):
        authenticate(is_staff=False)

        payload = {"title": "test"}
        response = api_client.post(GENRES_URL, payload)

        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_create_genre_empty_title(self, api_client, authenticate):
        authenticate(is_staff=True)

        payload = {"title": ""}
        response = api_client.post(GENRES_URL, payload)

        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_create_genre(self, api_client, authenticate):
        authenticate(is_staff=True)

        payload = {"title": "test"}
        response = api_client.post(GENRES_URL, payload)

        assert response.status_code == status.HTTP_201_CREATED
        assert response.data["title"] == payload["title"]

    def test_update_genre_empty_title(self, api_client, authenticate):
        authenticate(is_staff=True)

        genre = baker.make(Genre)

        payload = {"title": ""}
        response = api_client.put(genre_url(genre.id), payload)

        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_update_genre(self, api_client, authenticate):
        authenticate(is_staff=True)

        genre = baker.make(Genre)

        payload = {"title": "updated title"}
        response = api_client.put(genre_url(genre.id), payload)

        assert response.status_code == status.HTTP_200_OK
        assert response.data["title"] == payload["title"]

    def test_delete_genre(self, api_client, authenticate):
        authenticate(is_staff=True)

        genre = baker.make(Genre)
        response = api_client.delete(genre_url(genre.id))

        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert not Genre.objects.filter(id=genre.id).exists()
