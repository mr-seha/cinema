import pytest
from model_bakery import baker
from rest_framework import status

from movie.models import Collection


@pytest.mark.django_db
class TestCreateCollection:
    def test_if_user_is_anonymous_returns_401(self, api_client):
        response = api_client.post("/collections/", {"title": "test"})
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_if_user_is_not_admin_returns_403(self, api_client, authenticate):
        authenticate(is_staff=False)
        response = api_client.post("/collections/", {"title": "test"})
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_if_data_is_invalid_returns_400(self, api_client, authenticate):
        authenticate(is_staff=True)
        response = api_client.post("/collections/", {"title": ""})
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_if_data_is_valid_returns_201(self, api_client, authenticate):
        authenticate(is_staff=True)
        response = api_client.post("/collections/", {"title": "test"})
        assert response.status_code == status.HTTP_201_CREATED


@pytest.mark.django_db
class TestRetrieveCollection:
    def test_if_can_retrieve_collections_returns_200(self, api_client):
        response = api_client.get("/collections/")
        assert response.status_code == status.HTTP_200_OK

    def test_if_collection_exists_returns_200(self, api_client):
        collection = baker.make(Collection)
        response = api_client.get(f"/collections/{collection.id}/")
        assert response.status_code == status.HTTP_200_OK
        assert response.data['id'] == collection.id
        assert response.data['title'] == collection.title
