import django_setup

django_setup.setup_django_environment()


def print_users_to_console():
    from gallery.models import UserAccount

    for user in UserAccount.objects.all():
        print(user)


if __name__ == "__main__":
    print_users_to_console()
