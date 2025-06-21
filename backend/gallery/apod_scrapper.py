import logging
import os
from datetime import datetime

import google.generativeai as genai
import requests
from bs4 import BeautifulSoup
from bs4.element import Tag
from dotenv import load_dotenv

from .models import Gallery

logger = logging.getLogger(__name__)


def add_non_existing_images() -> None:
    a_tags = get_a_tags()

    for tag in a_tags:
        item = scrape_a_tag(tag)
        if item["image_url"] is None:
            continue

        item["date"] = convert_date(item["date"])
        try:
            Gallery.objects.get(date=item["date"])
            logger.info(f"{item['date']} is already in the database.")
            break
        except Gallery.DoesNotExist:
            logger.info(f"{item['date']} is not in the database.")
            entry = Gallery.objects.create(
                date=item["date"],
                title=item["title"],
                explanation=item["explanation"],
                image_url=item["image_url"],
                authors=item["authors"],
            )
            entry.save()


def convert_date(date: str) -> datetime.date:
    date = date.replace(":", "")
    return datetime.strptime(date, "%Y %B %d").date()


def get_a_tags() -> list[Tag]:
    source = requests.get("https://apod.nasa.gov/apod/archivepix.html").text
    soup = BeautifulSoup(source, "lxml")

    b_tag = soup.find_all("b")[1]
    return b_tag.find_all("a")


def scrape_a_tag(a_tag: Tag) -> dict:
    dictionary = {}

    date = a_tag.find_previous(string=True).strip()
    title = a_tag.text.strip()
    url = f"https://apod.nasa.gov/apod/{a_tag['href']}"
    image_url, explanation = get_image_and_explanation(url)
    authors = get_authors(url)

    dictionary["date"] = date
    dictionary["title"] = title
    dictionary["url"] = url
    dictionary["image_url"] = image_url
    dictionary["explanation"] = explanation
    dictionary["authors"] = authors

    return dictionary


def get_image_and_explanation(url: str) -> tuple[str, str]:
    source = requests.get(url).text
    soup = BeautifulSoup(source, "lxml")

    p_tags = soup.find_all("p")
    img_tag = soup.find("img")
    explanation = p_tags[2].get_text()

    try:
        image_url = f"https://apod.nasa.gov/apod/{img_tag['src']}"
    except Exception:
        image_url = None

    return image_url, explanation


def get_authors(url: str) -> str:
    source = requests.get(url).text
    soup = BeautifulSoup(source, "lxml")

    center_tags = soup.find_all("center")
    credit_center_tag = center_tags[1]
    authors = extract_authors_with_gemini(credit_center_tag)

    return authors


def extract_authors_with_gemini(center_tag: Tag) -> str:
    load_dotenv()
    genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

    query = f"""Given the following HTML code snippet, your role is to extract the credit information from the center tag.
The extracted credit information should be returned as a string and separated by a comma to denote multiple authors.
Dont't include prefix text like "Image Credit" or "Illustration Credit".

The HTML code snippet is as follows:
{center_tag}
"""

    model = genai.GenerativeModel("models/gemini-2.0-flash-001")
    response = model.generate_content(query)
    return response.text
