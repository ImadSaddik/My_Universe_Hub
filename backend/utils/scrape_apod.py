import json
import os
import time

import django_setup
from tqdm import tqdm

django_setup.setup_django_environment()


dir_path = os.path.dirname(os.path.realpath(__file__))  # /Development/backend/utils
backend_dir = os.path.abspath(os.path.join(dir_path, os.pardir))  # /Development/backend
data_path = os.path.join(backend_dir, "data", "apod_data.json")


def scrapeAPODWebsite() -> None:
    from gallery.apod_scrapper import get_a_tags, scrape_a_tag

    print("Scraping the APOD website.")
    createOutputFileIfNotExists()

    a_tags = get_a_tags()
    rpm_counter = 0
    start_time = time.time()
    for tag in tqdm(a_tags, total=len(a_tags)):
        try:
            item = scrape_a_tag(tag)
            if item["image_url"] is None:
                # This means that this is a video link, we don't want to include it
                continue

            with open(data_path, "r") as file:
                data = json.load(file)

            if itemExistsInData(data, item):
                print(f"Item for date {item['date']} already exists in the data. Stop scraping.")
                break
            else:
                data.append(item)

            # Write the updated data back to the file
            with open(data_path, "w") as file:
                json.dump(data, file, indent=4)

            # to avoid hitting the rate limit of 15 requests per minute
            end_time = time.time()
            if end_time - start_time < 60:
                rpm_counter += 1
                if rpm_counter == 10:  # 10 requests per minute just to leave a margin
                    time.sleep(60)
                    rpm_counter = 0
                    start_time = time.time()
        except Exception as e:
            print(f"An error occurred while scraping: {e}")
            continue


def createOutputFileIfNotExists() -> None:
    if not os.path.exists(data_path):
        with open(data_path, "w") as file:
            file.write("[]")


def itemExistsInData(data: list[dict], item: dict) -> bool:
    for entry in data:
        if entry["date"] == item["date"]:
            return True
    return False


if __name__ == "__main__":
    scrapeAPODWebsite()
