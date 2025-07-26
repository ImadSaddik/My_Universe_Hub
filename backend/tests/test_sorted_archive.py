import pytest
from django.urls import reverse
from gallery.models import Gallery
from rest_framework.test import APIClient
from utils import create_test_user, populate_database_with_test_data


@pytest.mark.django_db
def test_sorted_archive():
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

    # Now, fetch the sorted archive and check if the liked image is at the top
    start_index = 0
    end_index = 10
    url = reverse(viewname="get_sorted_archive", args=[start_index, end_index])
    response = client.get(url)

    assert response.status_code == 200  # type: ignore
    assert len(response.data) > 0  # type: ignore

    most_liked_image = response.data[0]  # type: ignore
    assert most_liked_image["date"] == date

    # Check that the rest of the images have 0 likes
    for item in response.data[1:]:  # type: ignore
        assert item["image_likes_count"] == 0, f"Expected 0 likes for {item['date']}, found {item['image_likes_count']}"


@pytest.mark.django_db
def test_sorted_archive_size():
    _ = populate_database_with_test_data()

    url = reverse(viewname="get_sorted_archive_size")
    client = APIClient()
    response = client.get(url)

    assert response.status_code == 200  # type: ignore
    assert "count" in response.data  # type: ignore
    assert response.data["count"] > 0, "Expected a positive count of sorted archive entries"  # type: ignore
