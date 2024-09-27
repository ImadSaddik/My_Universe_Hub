import os
import json
import django_setup
django_setup.setup_django_environment()

from tqdm import tqdm
from datetime import datetime
from gallery.models import Gallery


def fillDatabase(data):
    for item in tqdm(data, total=len(data)):
        if item['image_url'] == None:
            continue
        
        item['date'] = convertDate(item['date'])
        
        entry = Gallery.objects.create(
            date=item['date'],
            title=item['title'],
            explanation=item['explanation'],
            image_url=item['image_url'],
            authors=item['authors']
        )
        
        entry.save()
        
        
def convertDate(date):
    date = date.replace(':', '')
    return datetime.strptime(date, '%Y %B %d').date()


if __name__ == '__main__':
    dir_path = os.path.dirname(os.path.realpath(__file__)) # /Development/backend/utils
    backend_dir = os.path.abspath(os.path.join(dir_path, os.pardir)) # /Development/backend
    data_path = os.path.join(backend_dir, 'data', 'apod_data.json')
    with open(data_path, 'r') as file:
        data = json.load(file)
        
    fillDatabase(data)
