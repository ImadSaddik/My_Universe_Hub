import pytest
from django.urls import reverse
from rest_framework.test import APIClient

from utils import populate_database_with_test_data


@pytest.mark.django_db
def test_search_valid_input():
    populate_database_with_test_data()

    query = "Andromeda"
    start_index = 0
    end_index = 10
    url = reverse(viewname="search", args=[query, start_index, end_index])

    client = APIClient()
    response = client.get(url)
    assert response.status_code == 200
    assert all("Andromeda" in item["explanation"] for item in response.data)


@pytest.mark.django_db
def test_search_invalid_input():
    populate_database_with_test_data()

    query = "xx"
    start_index = 0
    end_index = 10
    url = reverse(viewname="search", args=[query, start_index, end_index])

    client = APIClient()
    response = client.get(url)
    assert response.status_code == 200
    assert len(response.data) == 0


@pytest.mark.django_db
def test_search_multiple_keywords():
    populate_database_with_test_data()

    query = "Eclipse,M31"
    start_index = 0
    end_index = 10
    url = reverse(viewname="search", args=[query, start_index, end_index])

    client = APIClient()
    response = client.get(url)
    assert response.status_code == 200
    # At least one result should match either Eclipse or M31
    assert any(("Eclipse" in item["explanation"] or "M31" in item["explanation"]) for item in response.data)


@pytest.mark.django_db
def test_search_size_valid_query():
    populate_database_with_test_data()

    query = "Andromeda"
    url = reverse(viewname="search_size", args=[query])
    client = APIClient()
    response = client.get(url)

    assert response.status_code == 200
    assert response.data["count"] > 0


@pytest.mark.django_db
def test_search_size_invalid_query():
    populate_database_with_test_data()

    query = "xxx"
    url = reverse(viewname="search_size", args=[query])
    client = APIClient()
    response = client.get(url)

    assert response.status_code == 200
    assert response.data["count"] == 0
