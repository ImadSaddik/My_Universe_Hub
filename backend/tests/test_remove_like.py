import pytest
from django.urls import reverse
from gallery.models import Gallery
from rest_framework.test import APIClient
from utils import create_test_user, populate_database_with_test_data


@pytest.mark.django_db
def test_unlike_image_valid():
    date = "2023-10-01"
    email = "test.e2e@example.com"

    _ = populate_database_with_test_data()
    user = create_test_user(email=email)

    # First like the image before unliking it
    client = APIClient()
    url = reverse("like_image")
    data = {"date": date, "email": email}
    response = client.post(url, data, format="json")

    assert response.status_code == 200  # type: ignore
    assert response.json()["message"] == "Image liked successfully!"  # type: ignore

    gallery = Gallery.objects.get(date=date)
    assert user in gallery.liked_by_users.all()

    # Unlike the image
    url = reverse(viewname="unlike_image")
    data = {"date": date, "email": email}
    response = client.post(url, data, format="json")

    assert response.status_code == 200  # type: ignore
    assert response.json()["message"] == "Image unliked successfully!"  # type: ignore

    gallery = Gallery.objects.get(date=date)
    assert user not in gallery.liked_by_users.all()


@pytest.mark.django_db
def test_unlike_image_invalid():
    date = "2069-10-01"
    email = "test.e2e@example.com"

    _ = populate_database_with_test_data()
    _ = create_test_user(email=email)

    client = APIClient()
    url = reverse(viewname="unlike_image")
    data = {"date": date, "email": email}
    response = client.post(url, data, format="json")

    assert response.status_code == 400  # type: ignore
    assert b"Something went wrong while unliking the image!" in response.content  # type: ignore
