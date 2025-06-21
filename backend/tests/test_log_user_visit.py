import pytest
from django.urls import reverse
from rest_framework.test import APIClient

from gallery.models import UserVisit
from utils import create_test_user


@pytest.mark.django_db
def test_log_user_visit_with_all_data():
    email = "test.e2e@example.com"
    user = create_test_user(email=email)

    client = APIClient()
    url = reverse(viewname="log_user_visit")
    data = {"email": email}
    response = client.post(url, data, format="json")

    assert response.status_code == 200
    assert response.json()["message"] == "Visit logged."

    all_user_visits = UserVisit.objects.all()
    assert len(all_user_visits) == 1
    assert all_user_visits[0].user == user


@pytest.mark.django_db
def test_log_user_visit_without_creating_user():
    email = "test.e2e@example.com"

    client = APIClient()
    url = reverse(viewname="log_user_visit")
    data = {"email": email}
    response = client.post(url, data, format="json")

    assert response.status_code == 400
    assert response.content.decode() == "User not found."

    all_user_visits = UserVisit.objects.all()
    assert len(all_user_visits) == 0


@pytest.mark.django_db
def test_log_user_visit_without_email():
    client = APIClient()
    url = reverse(viewname="log_user_visit")
    data = {"email": ""}
    response = client.post(url, data, format="json")

    assert response.status_code == 400
    assert response.content.decode() == "Email is required."

    all_user_visits = UserVisit.objects.all()
    assert len(all_user_visits) == 0
