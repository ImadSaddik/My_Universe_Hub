import os
from datetime import datetime

import django_setup
import google.generativeai as genai
import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv

django_setup.setup_django_environment()


def add_non_existing_images():
    from gallery.models import Gallery

    print("Adding non-existing entries to the database.")
    a_tags = get_a_tags()

    for tag in a_tags:
        item = scrape_a_tag(tag)
        if item["image_url"] is None:
            continue

        item["date"] = convert_date(item["date"])
        try:
            Gallery.objects.get(date=item["date"])
            print(f"{item['date']} is already in the database.")
            break
        except Gallery.DoesNotExist:
            print(f"{item['date']} is not in the database.")
            entry = Gallery.objects.create(
                date=item["date"],
                title=item["title"],
                explanation=item["explanation"],
                image_url=item["image_url"],
                authors=item["authors"],
            )

            entry.save()


def get_a_tags():
    source = requests.get("https://apod.nasa.gov/apod/archivepix.html").text
    soup = BeautifulSoup(source, "lxml")

    b_tag = soup.find_all("b")[1]
    return b_tag.find_all("a")


def scrape_a_tag(a_tag):
    dictionary = {}

    date = a_tag.find_previous(string=True).strip()
    title = a_tag.text.strip()
    url = f"https://apod.nasa.gov/apod/{a_tag['href']}"
    image, explanation = get_image_and_explanation(url)
    authors = get_authors(url)

    dictionary["date"] = date
    dictionary["title"] = title
    dictionary["url"] = url
    dictionary["image_url"] = image
    dictionary["explanation"] = explanation
    dictionary["authors"] = authors

    return dictionary


def get_image_and_explanation(url):
    source = requests.get(url).text
    soup = BeautifulSoup(source, "lxml")

    p_tags = soup.find_all("p")
    img_tag = soup.find("img")
    explanation = p_tags[2].get_text()

    try:
        img_url = f"https://apod.nasa.gov/apod/{img_tag['src']}"
    except Exception:
        img_url = None

    return img_url, explanation


def get_authors(url):
    source = requests.get(url).text
    soup = BeautifulSoup(source, "lxml")

    center_tags = soup.find_all("center")
    credit_center_tag = center_tags[1]
    authors = extract_authors_with_gemini(credit_center_tag)

    return authors


def extract_authors_with_gemini(center_tag):
    query = f"""Given the following HTML code snippet, your role is to extract the credit information from the center tag.
The extracted credit information should be returned as a string and separated by a comma to denote multiple authors.
Dont't include prefix text like "Image Credit" or "Illustration Credit".

The HTML code snippet is as follows:
{center_tag}
"""

    model = genai.GenerativeModel("models/gemini-2.0-flash")
    response = model.generate_content(query)
    return response.text


def convert_date(date):
    date = date.replace(":", "")
    return datetime.strptime(date, "%Y %B %d").date()


if __name__ == "__main__":
    load_dotenv()
    genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

    add_non_existing_images()
