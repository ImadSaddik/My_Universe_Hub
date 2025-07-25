import pytest
from django.urls import reverse
from gallery.models import UserVisit
from rest_framework.test import APIClient
from utils import create_test_user


@pytest.mark.django_db
def test_log_user_visit_with_all_data():
    email = "test.e2e@example.com"
    user = create_test_user(email=email)

    client = APIClient()
    url = reverse(viewname="log_user_visit")
    data = {"email": email}
    response = client.post(url, data, format="json")

    assert response.status_code == 200  # type: ignore
    assert response.json()["message"] == "Visit logged."  # type: ignore

    all_user_visits = UserVisit.objects.all()
    assert len(all_user_visits) == 1
    assert all_user_visits[0].user == user
    assert all_user_visits[0].ip_address == "127.0.0.1"


@pytest.mark.django_db
def test_log_user_visit_with_x_forwarded_for_single_ip():
    email = "test.xff1@example.com"
    user = create_test_user(email=email)

    client = APIClient()
    url = reverse(viewname="log_user_visit")
    data = {"email": email}
    headers = {"HTTP_X_FORWARDED_FOR": "203.0.113.1"}
    response = client.post(url, data, format="json", **headers)  # type: ignore

    assert response.status_code == 200  # type: ignore
    assert response.json()["message"] == "Visit logged."  # type: ignore

    visit = UserVisit.objects.last()
    assert visit.user == user  # type: ignore
    assert visit.ip_address == "203.0.113.1"  # type: ignore


@pytest.mark.django_db
def test_log_user_visit_with_x_forwarded_for_multiple_ips():
    email = "test.xff2@example.com"
    user = create_test_user(email=email)

    client = APIClient()
    url = reverse(viewname="log_user_visit")
    data = {"email": email}
    headers = {"HTTP_X_FORWARDED_FOR": "203.0.113.2, 70.41.3.18, 150.172.238.178"}
    response = client.post(url, data, format="json", **headers)  # type: ignore

    assert response.status_code == 200  # type: ignore
    assert response.json()["message"] == "Visit logged."  # type: ignore

    visit = UserVisit.objects.last()
    assert visit.user == user  # type: ignore
    assert visit.ip_address == "203.0.113.2"  # type: ignore


@pytest.mark.django_db
def test_log_user_visit_without_creating_user():
    email = "test.e2e@example.com"

    client = APIClient()
    url = reverse(viewname="log_user_visit")
    data = {"email": email}
    response = client.post(url, data, format="json")

    assert response.status_code == 400  # type: ignore
    assert response.content.decode() == "User not found."  # type: ignore

    all_user_visits = UserVisit.objects.all()
    assert len(all_user_visits) == 0


@pytest.mark.django_db
def test_log_user_visit_without_email():
    client = APIClient()
    url = reverse(viewname="log_user_visit")
    data = {"email": ""}
    response = client.post(url, data, format="json")

    assert response.status_code == 400  # type: ignore
    assert response.content.decode() == "Email is required."  # type: ignore

    all_user_visits = UserVisit.objects.all()
    assert len(all_user_visits) == 0
