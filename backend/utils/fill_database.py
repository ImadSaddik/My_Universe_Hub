import json
import os
from datetime import datetime

import django_setup
from tqdm import tqdm

django_setup.setup_django_environment()


def fillDatabase(data):
    from gallery.models import Gallery

    for item in tqdm(data, total=len(data)):
        if item["image_url"] is None:
            continue

        item["date"] = convert_date(item["date"])

        entry = Gallery.objects.create(
            date=item["date"],
            title=item["title"],
            explanation=item["explanation"],
            image_url=item["image_url"],
            authors=item["authors"],
        )

        entry.save()


def convert_date(date):
    date = date.replace(":", "")
    return datetime.strptime(date, "%Y %B %d").date()


if __name__ == "__main__":
    dir_path = os.path.dirname(os.path.realpath(__file__))  # /Development/backend/utils
    backend_dir = os.path.abspath(os.path.join(dir_path, os.pardir))  # /Development/backend
    data_path = os.path.join(backend_dir, "data", "apod_data.json")
    with open(data_path, "r") as file:
        data = json.load(file)

    fillDatabase(data)
