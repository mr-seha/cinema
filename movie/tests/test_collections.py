import pytest
from model_bakery import baker
from rest_framework import status

from movie.models import Collection

COLLECTIONS_URL = "/api/collections/"


@pytest.fixture
def create_collection(api_client):
    def do_create_collection(title="test title"):
        return api_client.post(COLLECTIONS_URL, {"title": title})

    return do_create_collection


@pytest.fixture
def delete_collection(api_client):
    def do_delete_collection(id):
        return api_client.delete(COLLECTIONS_URL + f"{id}/")

    return do_delete_collection


@pytest.fixture
def update_collection(api_client):
    def do_update_collection(collection_id, title="test title"):
        return api_client.put(COLLECTIONS_URL + f"{collection_id}/", {"title": title})

    return do_update_collection


@pytest.mark.django_db
class TestCreateCollection:
    def test_user_is_anonymous(self, api_client, create_collection):
        response = create_collection()
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_user_is_not_admin(self, api_client, authenticate, create_collection):
        authenticate(is_staff=False)
        response = create_collection()
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_data_is_invalid(self, api_client, authenticate, create_collection):
        authenticate(is_staff=True)
        response = create_collection(title="")
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_data_is_valid(self, api_client, authenticate, create_collection):
        authenticate(is_staff=True)
        response = create_collection()
        assert response.status_code == status.HTTP_201_CREATED


@pytest.mark.django_db
class TestRetrieveCollection:
    def test_retrieve_collections(self, api_client):
        response = api_client.get(COLLECTIONS_URL)
        assert response.status_code == status.HTTP_200_OK

    def test_retrieve_a_collection(self, api_client):
        collection = baker.make(Collection)

        response = api_client.get(COLLECTIONS_URL + f"{collection.id}/")

        assert response.status_code == status.HTTP_200_OK
        assert response.data["id"] == collection.id
        assert response.data["title"] == collection.title


@pytest.mark.django_db
class TestDeleteCollection:
    def test_user_is_anonymous(self, api_client, delete_collection):
        collection = baker.make(Collection)
        response = delete_collection(collection.id)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_user_is_not_admin(self, api_client, authenticate, delete_collection):
        authenticate(is_staff=False)
        collection = baker.make(Collection)
        response = delete_collection(collection.id)
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_delete_collection_success(self, api_client, authenticate, delete_collection):
        authenticate(is_staff=True)
        collection = baker.make(Collection)
        response = delete_collection(collection.id)
        assert response.status_code == status.HTTP_204_NO_CONTENT

        response = api_client.get(COLLECTIONS_URL + f"{collection.id}/")
        assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.django_db
class TestUpdateCollection:
    def test_user_is_anonymous(self, api_client, update_collection):
        collection = baker.make(Collection)

        response = update_collection(collection.id, "test")
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

        response = api_client.get(COLLECTIONS_URL + f"{collection.id}/")
        assert response.data["title"] == collection.title

    def test_user_is_not_admin(self, api_client, authenticate, update_collection):
        authenticate(is_staff=False)
        collection = baker.make(Collection)

        response = update_collection(collection.id, "test")
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_data_is_invalid(self, api_client, authenticate, update_collection):
        authenticate(is_staff=True)
        collection = baker.make(Collection)

        response = update_collection(collection.id, "")
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_user_is_admin(self, api_client, authenticate, update_collection):
        authenticate(is_staff=True)
        collection = baker.make(Collection)

        new_title = "test new title"

        response = update_collection(collection.id, new_title)
        assert response.status_code == status.HTTP_200_OK

        response = api_client.get(COLLECTIONS_URL + f"{collection.id}/")
        assert response.data["title"] == new_title
