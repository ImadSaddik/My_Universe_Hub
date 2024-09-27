import os
import json
import django_setup
django_setup.setup_django_environment()

from datetime import datetime
from gallery.models import Gallery


def fillDatabase(data):
    for item in data:
        if item['image'] == None:
            continue
        
        date = item['date'].replace(':', '')
        dateAfter = datetime.strptime(date, '%Y %B %d')
        item['date'] = dateAfter.strftime('%Y-%m-%d')
        
        entry = Gallery.objects.create(
            date=item['date'],
            title=item['title'],
            explanation=item['explanation'],
            image_url=item['image'],
            authors=item['authors']
        )
        
        entry.save()


if __name__ == '__main__':
    dir_path = os.path.dirname(os.path.realpath(__file__)) # /Development/backend/utils
    backend_dir = os.path.abspath(os.path.join(dir_path, os.pardir)) # /Development/backend
    data_path = os.path.join(backend_dir, 'data', 'apod_data.json')
    with open(data_path, 'r') as file:
        data = json.load(file)
        
    fillDatabase(data)
