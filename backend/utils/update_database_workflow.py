import django_setup

django_setup.setup_django_environment()


def add_non_existing_images() -> None:
    from gallery.apod_scrapper import convert_date, get_a_tags, scrape_a_tag
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


if __name__ == "__main__":
    add_non_existing_images()
