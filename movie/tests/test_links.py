import pytest
from model_bakery import baker
from rest_framework import status

from movie.models import Link


@pytest.mark.django_db
class TestRetrieveLink:
    def test_if_user_is_anonymous_returns_401(self, api_client):
        response = api_client.get("/links/")
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_if_user_is_not_admin_returns_403(self, api_client, authenticate):
        authenticate(is_staff=False)
        response = api_client.get("/links/")
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_if_link_exists_returns_200(self, api_client, authenticate):
        link = baker.make(Link)
        authenticate(is_staff=True)
        response = api_client.get(f"/links/{link.id}/")
        assert response.status_code == status.HTTP_200_OK
        assert response.data['id'] == link.id
