import pytest
from model_bakery import baker
from rest_framework import status

from movie.models import Actor

ACTORS_URL = "/api/actors/"


@pytest.fixture
def create_actor(api_client):
    def do_create_actor(full_name="reza", full_name_en="rezayi"):
        return api_client.post(
            ACTORS_URL,
            {"full_name": full_name, "full_name_en": full_name_en}
        )

    return do_create_actor


@pytest.fixture
def delete_actor(api_client):
    def do_delete_actor(actor_id):
        return api_client.delete(ACTORS_URL + f"{actor_id}/")

    return do_delete_actor


@pytest.fixture
def update_actor(api_client):
    def do_update_actor(actor_id, full_name="reza", full_name_en="rezayi"):
        return api_client.patch(
            ACTORS_URL + f"{actor_id}/",
            {"full_name": full_name, "full_name_en": full_name_en}
        )

    return do_update_actor


@pytest.mark.django_db
class TestCreateActor:
    def test_user_is_anonymous(self, api_client, create_actor):
        response = create_actor()
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_user_is_not_admin(self, api_client, authenticate, create_actor):
        authenticate(is_staff=False)
        response = create_actor()
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_data_is_invalid(self, api_client, authenticate, create_actor):
        authenticate(is_staff=True)
        response = create_actor(full_name="")
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_data_is_valid(self, api_client, authenticate, create_actor):
        authenticate(is_staff=True)
        response = create_actor()
        assert response.status_code == status.HTTP_201_CREATED


@pytest.mark.django_db
class TestRetrieveActor:
    def test_retrieve_actors(self, api_client):
        response = api_client.get(ACTORS_URL)
        assert response.status_code == status.HTTP_200_OK

    def test_retrieve_a_actor(self, api_client):
        actor = baker.make(Actor)

        response = api_client.get(ACTORS_URL + f"{actor.id}/")

        assert response.status_code == status.HTTP_200_OK
        assert response.data['id'] == actor.id
        assert response.data['full_name'] == actor.full_name
        assert response.data['full_name_en'] == actor.full_name_en


@pytest.mark.django_db
class TestDeleteActor:
    def test_user_is_anonymous(self, api_client, delete_actor):
        actor = baker.make(Actor)
        response = delete_actor(actor.id)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_user_is_not_admin(self, api_client, authenticate, delete_actor):
        authenticate(is_staff=False)
        actor = baker.make(Actor)
        response = delete_actor(actor.id)
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_delete_actor_success(self, api_client, authenticate, delete_actor):
        authenticate(is_staff=True)
        actor = baker.make(Actor)
        response = delete_actor(actor.id)
        assert response.status_code == status.HTTP_204_NO_CONTENT

        response = api_client.get(ACTORS_URL + f"{actor.id}/")
        assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.django_db
class TestUpdateActor:
    def test_user_is_anonymous(self, api_client, update_actor):
        actor = baker.make(Actor)

        response = update_actor(actor.id, "ahmad")
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

        response = api_client.get(ACTORS_URL + f"{actor.id}/")
        assert response.data["full_name"] == actor.full_name
        assert response.data["full_name_en"] == actor.full_name_en

    def test_user_is_not_admin(self, api_client, authenticate, update_actor):
        authenticate(is_staff=False)
        actor = baker.make(Actor)

        response = update_actor(actor.id, "ali")
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_data_is_invalid(self, api_client, authenticate, update_actor):
        authenticate(is_staff=True)
        actor = baker.make(Actor)

        response = update_actor(actor.id, "")
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_user_is_admin(self, api_client, authenticate, update_actor):
        authenticate(is_staff=True)
        actor = baker.make(Actor)

        new_full_name = "ahmad"

        response = update_actor(actor.id, new_full_name)
        assert response.status_code == status.HTTP_200_OK

        response = api_client.get(ACTORS_URL + f"{actor.id}/")
        assert response.data["full_name"] == new_full_name
