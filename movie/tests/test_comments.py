import pytest
from django.urls import reverse
from model_bakery import baker
from rest_framework import status

from movie.models import Comment, Film
from movie.views import CommentNestedViewSet


def film_url(film_id):
    return reverse("movie:films-detail", args=[film_id])


@pytest.mark.django_db
class TestPrivateFilmCommentsAPI:
    def test_delete_comment(self, api_client, authenticate):
        film = baker.make(Film)
        comment = baker.make(Comment, film=film)

        authenticate(is_staff=True)

        response = api_client.delete(
            film_url(film.id) + f"comments/{comment.id}/"
        )
        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert not Comment.objects.filter(id=comment.id).exists()

    def test_update_comment(self, api_client, authenticate):
        film = baker.make(Film)
        comment = baker.make(Comment, film=film)

        authenticate(is_staff=True)

        payload = {"text": "Updated comment!", "rating": 4}
        response = api_client.patch(
            film_url(film.id) + f"comments/{comment.id}/",
            payload
        )
        assert response.status_code == status.HTTP_200_OK
        assert response.data["text"] == payload["text"]
        assert response.data["rating"] == payload["rating"]


@pytest.mark.django_db
class TestPublicFilmCommentsAPI:
    def test_user_is_anonymous(self, api_client):
        film = baker.make(Film)
        payload = {"text": "Awesome!", "rating": 5, }

        response = api_client.post(film_url(film.id) + "comments/", payload)

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_create_comment_empty_text(self, api_client, authenticate):
        authenticate(is_staff=False)

        film = baker.make(Film)

        payload = {"text": "", "rating": 5}
        response = api_client.post(film_url(film.id) + "comments/", payload)
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_create_comment_no_rating(self, api_client, authenticate):
        authenticate(is_staff=False)

        film = baker.make(Film)

        payload = {"text": "Awesome"}
        response = api_client.post(film_url(film.id) + "comments/", payload)
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_delete_comment_forbidden(self, api_client, authenticate):
        film = baker.make(Film)
        comment = baker.make(Comment, film=film)

        authenticate(is_staff=False)

        response = api_client.delete(
            film_url(film.id) + f"comments/{comment.id}/"
        )
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_update_comment_forbidden(self, api_client, authenticate):
        film = baker.make(Film)
        comment = baker.make(Comment, film=film)

        authenticate(is_staff=False)

        payload = {"text": "Update forbidden"}
        response = api_client.patch(
            film_url(film.id) + f"comments/{comment.id}/",
            payload
        )
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_add_comment(self, api_client, authenticate, mocker):
        authenticate(is_staff=False)
        film = baker.make(Film)

        mocker.patch.object(
            CommentNestedViewSet,
            'get_serializer_context',
            return_value={"film_id": film.id, "user_id": 1})

        payload = {"text": "Awesome", "rating": 5}
        response = api_client.post(film_url(film.id) + "comments/", payload)
        assert response.status_code == status.HTTP_201_CREATED
