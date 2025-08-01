import os

import django_setup
from dotenv import load_dotenv

load_dotenv()
django_setup.setup_django_environment()


def create_test_user():
    from gallery.models import UserAccount

    email = os.getenv("TEST_USER_EMAIL")
    password = os.getenv("TEST_USER_PASSWORD")
    name = "Test User"

    if UserAccount.objects.filter(email=email).exists():
        print(f"Test user {email} already exists")
        return

    _ = UserAccount.objects.create_user(email=email, name=name, password=password)  # type: ignore
    print(f"Created test user: {email}")


if __name__ == "__main__":
    create_test_user()
