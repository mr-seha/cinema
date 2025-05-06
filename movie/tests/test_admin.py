import pytest
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status

ADMIN_FILM_URL = reverse("admin:movie_film_changelist")


@pytest.mark.django_db
class TestAdmin:
    def test_film_list(self, api_client, authenticate):
        admin_user_payload = dict(
            username="admin",
            email="admin@gmail.com",
            password="admin_password",
            is_staff=True,
        )

        user = get_user_model().objects.create_superuser(**admin_user_payload)
        api_client.force_login(user=user)

        response = api_client.get(ADMIN_FILM_URL)

        assert response.status_code == status.HTTP_200_OK
        assert "IMDB" in response.text
