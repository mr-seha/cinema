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

        payload = {"text": "Updated comment!"}
        response = api_client.patch(
            film_url(film.id) + f"comments/{comment.id}/",
            payload
        )
        assert response.status_code == status.HTTP_200_OK
        assert response.data["text"] == payload["text"]


@pytest.mark.django_db
class TestPublicFilmCommentsAPI:
    def test_user_is_anonymous(self, api_client):
        film = baker.make(Film)
        payload = {"text": "Awesome!"}

        response = api_client.post(film_url(film.id) + "comments/", payload)

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_create_comment_empty_text(self, api_client, authenticate):
        authenticate(is_staff=False)

        film = baker.make(Film)

        payload = {"text": ""}
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

        payload = {"text": "Awesome"}
        response = api_client.post(film_url(film.id) + "comments/", payload)
        assert response.status_code == status.HTTP_201_CREATED

    def test_like_comment(self, api_client):
        film = baker.make(Film)
        comment = baker.make(
            Comment,
            film=film,
            status=Comment.STATUS_APPROVED
        )

        url = film_url(film.id) + f"comments/{comment.id}/like/"
        response1 = api_client.post(url)
        response2 = api_client.post(url)

        assert response1.status_code == status.HTTP_200_OK
        assert response2.status_code == status.HTTP_400_BAD_REQUEST

        comment.refresh_from_db()
        assert comment.like_count == 1

    def test_dislike_comment(self, api_client):
        film = baker.make(Film)
        comment = baker.make(
            Comment,
            film=film,
            status=Comment.STATUS_APPROVED
        )

        url = film_url(film.id) + f"comments/{comment.id}/dislike/"
        response1 = api_client.post(url)
        response2 = api_client.post(url)

        assert response1.status_code == status.HTTP_200_OK
        assert response2.status_code == status.HTTP_400_BAD_REQUEST

        comment.refresh_from_db()
        assert comment.dislike_count == 1

    def test_not_show_rejected_comments_to_non_admins(self, api_client):
        film = baker.make(Film)
        comment = baker.make(
            Comment,
            film=film,
            status=Comment.STATUS_APPROVED
        )
        baker.make(
            Comment,
            film=film,
            status=Comment.STATUS_REJECTED
        )

        response = api_client.get(film_url(film.id) + "comments/")

        assert len(response.data["results"]) == 1
        assert response.data["results"][0]["text"] == comment.text
