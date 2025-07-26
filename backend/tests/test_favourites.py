import pytest
from django.urls import reverse
from gallery.models import Gallery
from rest_framework.test import APIClient
from utils import create_test_user, populate_database_with_test_data


@pytest.mark.django_db
def test_no_favourites():
    email = "test.e2e@example.com"

    _ = populate_database_with_test_data()
    _ = create_test_user(email=email)

    start_index = 0
    end_index = 10
    url = reverse(viewname="get_favourites_archive", args=[email, start_index, end_index])

    client = APIClient()
    response = client.get(url)

    assert response.status_code == 200  # type: ignore
    assert len(response.data) == 0  # type: ignore


@pytest.mark.django_db
def test_available_favourites():
    date = "2023-10-01"
    email = "test.e2e@example.com"

    _ = populate_database_with_test_data()
    user = create_test_user(email=email)

    # First like the image
    client = APIClient()
    url = reverse(viewname="like_image")
    data = {"date": date, "email": email}
    response = client.post(url, data, format="json")

    assert response.status_code == 200  # type: ignore
    assert response.json()["message"] == "Image liked successfully!"  # type: ignore

    gallery = Gallery.objects.get(date=date)
    assert user in gallery.liked_by_users.all()

    # Now, fetch the favourites archive
    start_index = 0
    end_index = 10
    url = reverse(viewname="get_favourites_archive", args=[email, start_index, end_index])
    response = client.get(url)

    assert response.status_code == 200  # type: ignore
    assert len(response.data) == 1  # type: ignore


@pytest.mark.django_db
def test_no_favourites_size():
    _ = populate_database_with_test_data()

    email = "test.e2e@example.com"
    _ = create_test_user(email=email)

    url = reverse(viewname="get_favourites_archive_size", args=[email])
    client = APIClient()
    response = client.get(url)

    assert response.status_code == 200  # type: ignore
    assert "count" in response.data  # type: ignore
    assert response.data["count"] == 0, "Expected a count of 0 for favourites when no images are liked"  # type: ignore


@pytest.mark.django_db
def test_available_favourites_size():
    date = "2023-10-01"
    email = "test.e2e@example.com"

    _ = populate_database_with_test_data()
    user = create_test_user(email=email)

    # First like the image
    client = APIClient()
    url = reverse(viewname="like_image")
    data = {"date": date, "email": email}
    response = client.post(url, data, format="json")

    assert response.status_code == 200  # type: ignore
    assert response.json()["message"] == "Image liked successfully!"  # type: ignore

    gallery = Gallery.objects.get(date=date)
    assert user in gallery.liked_by_users.all()

    # Now, fetch the favourites archive size
    url = reverse(viewname="get_favourites_archive_size", args=[email])
    client = APIClient()
    response = client.get(url)

    assert response.status_code == 200  # type: ignore
    assert "count" in response.data  # type: ignore
    assert response.data["count"] == 1  # type: ignore
