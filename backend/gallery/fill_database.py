import pickle
from gallery.models import Keyword, Gallery
from datetime import datetime

with open('/home/imad/Projects/APOD/website/backend/gallery/archive.pickle', 'rb') as f:
    archive = pickle.load(f)
    
for item in archive:
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
    )
    
    entry.save()

