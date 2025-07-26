import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from utils import create_test_user


@pytest.mark.django_db
def test_reset_password_success():
    email = "test.e2e@example.com"
    user = create_test_user(email=email)

    client = APIClient()
    url = reverse(viewname="reset_password")
    data = {"email": email, "newPassword": "new_secure_password"}
    response = client.post(url, data, format="json")

    assert response.status_code == 200  # type: ignore
    assert response.json()["message"] == "Password reset successfully!"  # type: ignore

    user.refresh_from_db()
    assert user.check_password("new_secure_password") is True, "Password was not updated correctly"


@pytest.mark.django_db
def test_reset_password_failure():
    client = APIClient()
    url = reverse(viewname="reset_password")
    data = {"email": "test@example.com", "newPassword": "new_secure_password"}
    response = client.post(url, data, format="json")

    assert response.status_code == 400  # type: ignore
    assert b"User not found!" in response.content  # type: ignore
