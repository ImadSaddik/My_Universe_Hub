import logging
import os
import textwrap
from datetime import date, datetime

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


def convert_date(date_str: str) -> date:
    date_str = date_str.replace(":", "")
    return datetime.strptime(date_str, "%Y %B %d").date()


def get_a_tags() -> list[Tag]:
    source = requests.get("https://apod.nasa.gov/apod/archivepix.html").text
    soup = BeautifulSoup(source, "lxml")

    b_tag = soup.find_all("b")[1]
    return b_tag.find_all("a")


def scrape_a_tag(a_tag: Tag) -> dict:
    dictionary = {}

    date_str = a_tag.find_previous(string=True).strip()  # type: ignore
    title = a_tag.text.strip()
    url = f"https://apod.nasa.gov/apod/{a_tag['href']}"
    image_url, explanation = get_image_and_explanation(url)
    authors = get_authors(url)

    dictionary["date"] = date_str
    dictionary["title"] = title
    dictionary["url"] = url
    dictionary["image_url"] = image_url
    dictionary["explanation"] = explanation
    dictionary["authors"] = authors

    return dictionary


def get_image_and_explanation(url: str) -> tuple[str | None, str]:
    source = requests.get(url).text
    soup = BeautifulSoup(source, "lxml")

    p_tags = soup.find_all("p")
    img_tag = soup.find("img")
    explanation = p_tags[2].get_text()

    try:
        image_url = f"https://apod.nasa.gov/apod/{img_tag['src']}"  # type: ignore
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


def extract_authors_with_gemini(html_code_to_process: Tag) -> str:
    load_dotenv()
    genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

    system_prompt = textwrap.dedent(f"""
    You are an expert text extraction AI. Your sole purpose is to extract author and credit information from a snippet of HTML code.

    Follow these rules precisely:
    1.  Find the text that comes **after** the "Image Credit" or "Illustration Credit" line.
    2.  Extract all names and sources, including the text inside `<a>` tags.
    3.  Combine everything into a **single string**.
    4.  Replace any semicolons (`;`) with commas (`,`).

    **CRITICAL:** Your response must **only** be the final extracted string. Do not write explanations, code, or any other text.

    ---

    ### Example 1

    **Input HTML:**
    ```html
    <center>
    <b> The Great Globular Cluster in Hercules </b> <br/>
    <b>Image Credit &amp;
    <a href="lib/about_apod.html#srapply">Copyright</a>:</b>
    <a href="[https://www.distant-luminosity.com/about.html](https://www.distant-luminosity.com/about.html)">Jan Beckmann, Julian Zoller, Lukas Eisert, Wolfgang Hummel</a>
    </center>
    ````

    **Output:**
    Jan Beckmann, Julian Zoller, Lukas Eisert, Wolfgang Hummel

    -----

    ### Example 2

    **Input HTML:**

    ```html
    <center>
    <b> NGC 602: Oyster Star Cluster </b> <br>
    <b> Image Credit: </b>
    X-ray: Chandra: NASA/CXC/Univ.Potsdam/L.Oskinova et al; <br>
    Optical: Hubble: NASA/STScI; Infrared: Spitzer: NASA/JPL-Caltech
    </center>
    ```

    **Output:**
    X-ray: Chandra: NASA/CXC/Univ.Potsdam/L.Oskinova et al, Optical: Hubble: NASA/STScI, Infrared: Spitzer: NASA/JPL-Caltech

    -----

    Now, process the following HTML.

    **Input HTML:**

    ```html
    {html_code_to_process}
    ```

    **Output:**
    """)

    model = genai.GenerativeModel("models/gemini-2.5-flash")
    response = model.generate_content(system_prompt)
    return response.text
