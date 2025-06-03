import pytest
from django.urls import reverse
from rest_framework.test import APIClient

from gallery.models import Gallery
from utils import create_test_user, populate_database_with_test_data


@pytest.mark.django_db
def test_like_image_valid():
    date = "2023-10-01"
    email = "test.e2e@example.com"

    _ = populate_database_with_test_data()
    user = create_test_user(email=email)

    client = APIClient()
    url = reverse(viewname="like_image")
    data = {"date": date, "email": email}
    response = client.post(url, data, format="json")

    assert response.status_code == 200
    assert response.json()["message"] == "Image liked successfully!"

    gallery = Gallery.objects.get(date=date)
    assert user in gallery.liked_by_users.all()


@pytest.mark.django_db
def test_like_image_invalid():
    date = "2069-10-01"
    email = "test.e2e@example.com"

    _ = populate_database_with_test_data()
    _ = create_test_user(email=email)

    client = APIClient()
    url = reverse(viewname="like_image")
    data = {"date": date, "email": email}
    response = client.post(url, data, format="json")

    assert response.status_code == 400
    assert b"Image not found" in response.content
