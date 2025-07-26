import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from utils import populate_database_with_test_data


@pytest.mark.django_db
def test_get_archive_data():
    count = populate_database_with_test_data()

    start_index = 0
    end_index = 10
    url = reverse(viewname="get_archive", args=[start_index, end_index])

    client = APIClient()
    response = client.get(url)
    assert response.status_code == 200  # type: ignore
    assert len(response.data) == count  # type: ignore


@pytest.mark.django_db
def test_get_archive_count():
    count = populate_database_with_test_data()

    url = reverse(viewname="get_archive_size")
    client = APIClient()
    response = client.get(url)
    assert response.status_code == 200  # type: ignore
    assert response.data["count"] == count  # type: ignore
