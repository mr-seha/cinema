import pytest
from django.contrib.auth import get_user_model
from django.urls import reverse
from model_bakery import baker
from rest_framework import status
from rest_framework.test import APIClient

PROFILE_URL = reverse("core:user-profile")


@pytest.fixture
def sample_user_data():
    def get_sample_user_data(**kwargs):
        return {
            "username": kwargs.get("username", "test"),
            "email": kwargs.get("email", "test@gmail.com"),
            "password": kwargs.get("password", "test123456"),
            "confirm_password": kwargs.get("confirm_password", "test123456")
        }

    return get_sample_user_data


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def register_user(api_client, sample_user_data):
    def do_register_user(**kwargs):
        register_url = reverse("core:user-register")
        payload = sample_user_data(**kwargs)
        return api_client.post(register_url, payload)

    return do_register_user


@pytest.fixture
def create_user():
    def do_create_user(**kwargs):
        return baker.make(get_user_model(), **kwargs)

    return do_create_user


@pytest.fixture
def authenticated_client(create_user):
    user = create_user()
    client = APIClient()
    client.force_authenticate(user=user)
    return client, user


@pytest.mark.django_db
class TestPublicUserAPI:
    def test_user_registration_successful(self, register_user):
        response = register_user()
        assert response.status_code == status.HTTP_201_CREATED
        assert get_user_model().objects.count() == 1

    def test_register_user_with_existing_username_fails(
            self,
            create_user,
            register_user
    ):
        user = create_user()
        response = register_user(username=user.get_username())

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert get_user_model().objects.count() == 1

    def test_register_user_with_existing_email_fails(
            self,
            create_user,
            register_user
    ):
        user = create_user()
        response = register_user(email=user.email)

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert get_user_model().objects.count() == 1

    def test_register_user_with_weak_password_fails(self, register_user):
        password = "1234"
        response = register_user(password=password, confirm_password=password)

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert get_user_model().objects.count() == 0

    def test_registration_fails_on_password_mismatch(self, register_user):
        password = "password12453"
        confirm_password = "not_match_pass"
        response = register_user(
            password=password,
            confirm_password=confirm_password
        )

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert get_user_model().objects.count() == 0


@pytest.mark.django_db
class TestPrivateUserAPI:
    def test_get_user_tokens(self, create_user):
        user = create_user()
        user.set_password(password := "1234578test")
        user.save()

        payload = {"username": user.get_username(), "password": password}
        response = APIClient().post("/api/token/", payload)

        assert response.status_code == status.HTTP_200_OK
        assert "access" in response.data
        assert "refresh" in response.data

    def test_authenticated_user_can_view_profile_page(
            self,
            authenticated_client
    ):
        api_client, user = authenticated_client

        response = api_client.get(PROFILE_URL)
        assert response.status_code == status.HTTP_200_OK

    def test_authenticated_user_can_update_profile(self, authenticated_client):
        api_client, user = authenticated_client

        payload = {
            "username": "new_username",
            "email": "test@gmail.com"
        }

        response = api_client.patch(PROFILE_URL, payload)
        assert response.status_code == status.HTTP_200_OK

        user.refresh_from_db()
        assert user.get_username() == payload["username"]
        assert user.email == payload["email"]

    def test_authenticated_user_can_update_password(
            self,
            authenticated_client
    ):
        api_client, user = authenticated_client

        payload = {
            "password": "new_pass12345",
            "confirm_password": "new_pass12345"
        }

        response = api_client.patch(PROFILE_URL, payload)
        assert response.status_code == status.HTTP_200_OK

        user.refresh_from_db()
        assert user.check_password(payload["password"])
