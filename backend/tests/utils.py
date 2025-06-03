from gallery.models import Gallery, UserAccount


def populate_database_with_test_data() -> int:
    Gallery.objects.create(
        date="2023-10-01",
        title="Andromeda Galaxy",
        explanation="The Andromeda Galaxy is a spiral galaxy approximately 2.537 million light-years from Earth.",
        image_url="https://example.com/andromeda.jpg",
        authors="NASA, ESA",
    )

    Gallery.objects.create(
        date="2023-10-02",
        title="Mars Exploration",
        explanation="Mars is the fourth planet from the Sun and is known for its red appearance.",
        image_url="https://example.com/mars.jpg",
        authors="NASA",
    )

    Gallery.objects.create(
        date="2023-10-03",
        title="M31",
        explanation="M31, also known as the Andromeda Galaxy, is the nearest spiral galaxy to the Milky Way.",
        image_url="https://example.com/m31.jpg",
        authors="ESA",
    )

    Gallery.objects.create(
        date="2023-10-04",
        title="Lunar Eclipse",
        explanation="A lunar eclipse occurs when the Earth passes between the Sun and the Moon.",
        image_url="https://example.com/lunar_eclipse.jpg",
        authors="NASA",
    )

    return len(Gallery.objects.all())


def create_test_user(email: str = "test@example.com") -> UserAccount:
    user = UserAccount.objects.create(email=email)
    return user
