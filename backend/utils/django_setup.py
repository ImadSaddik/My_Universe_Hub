import os
import sys
import django


def setup_django_environment():
    dir_path = os.path.dirname(os.path.realpath(__file__))  # /Development/backend/utils
    backend_dir = os.path.abspath(os.path.join(dir_path, os.pardir))  # /Development/backend
    project_dir = os.path.abspath(os.path.join(backend_dir, os.pardir))  # /Development

    sys.path.insert(0, project_dir)
    sys.path.insert(0, backend_dir)
    sys.path.insert(0, os.path.join(backend_dir, "backend"))

    os.environ["DJANGO_SETTINGS_MODULE"] = "backend.settings"
    django.setup()
