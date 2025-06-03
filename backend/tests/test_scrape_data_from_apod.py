import datetime

import pytest
from bs4.element import Tag

from gallery.apod_scrapper import convert_date, get_a_tags, get_authors, get_image_and_explanation, scrape_a_tag


@pytest.fixture
def a_tags() -> list[Tag]:
    return get_a_tags()


@pytest.fixture
def apod_entry_url(a_tags: list[Tag]) -> str:
    href = a_tags[0].get("href")
    return f"https://apod.nasa.gov/apod/{href}"


def test_scrapping_a_tags(a_tags: list[Tag]) -> None:
    assert len(a_tags) > 0, "No a tags found"

    all_tags_are_bs4_tag = all(isinstance(tag, Tag) for tag in a_tags)
    assert all_tags_are_bs4_tag, "Not all a tags are of type Tag"


def test_scrape_a_tag(a_tags: list[Tag]) -> None:
    dictionary = scrape_a_tag(a_tag=a_tags[0])
    assert "date" in dictionary
    assert "title" in dictionary
    assert "url" in dictionary
    assert "image_url" in dictionary
    assert "explanation" in dictionary
    assert "authors" in dictionary


def test_get_image_and_explanation(apod_entry_url: str) -> None:
    image_url, explanation = get_image_and_explanation(url=apod_entry_url)

    assert image_url is not None, "Image URL should not be None"
    assert explanation is not None, "Explanation should not be None"

    assert isinstance(image_url, str), "Image URL should be a string"
    assert isinstance(explanation, str), "Explanation should be a string"


def test_get_authors(apod_entry_url: str) -> None:
    authors = get_authors(url=apod_entry_url)

    assert authors is not None, "Authors should not be None"
    assert isinstance(authors, str), "Authors should be a string"
    assert len(authors) > 0, "Authors string should not be empty"


def test_convert_date() -> None:
    date_str = "2025 June 03:"
    converted_date = convert_date(date=date_str)

    assert isinstance(converted_date, datetime.date), "Converted date should be a datetime.date object"
    assert converted_date.year == 2025, "Year should be 2025"
    assert converted_date.month == 6, "Month should be June"
    assert converted_date.day == 3, "Day should be 3"
