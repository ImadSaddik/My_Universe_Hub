import json
import requests
from bs4 import BeautifulSoup
from datetime import datetime

from django.http import JsonResponse

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view

from .models import Gallery
from .serializers import GallerySerializer


class getArchive(APIView):
    def get(self, request, format=None):
        # addTodayPictureIfPossible()
        
        entries = Gallery.objects.all()
        serializer = GallerySerializer(entries, many=True)
        
        return Response(serializer.data)
    
    
def addTodayPictureIfPossible():
    response = getTodayPicture(request=None)
    item = json.loads(response.content)
    item['date'] = convertDate(item['date'])
    
    try:
        Gallery.objects.get(date=item['date'])
        print("Today's picture is already in the database.")
    except:
        print("Today's picture is not in the database.")
        entry = Gallery.objects.create(
            date=item['date'],
            title=item['title'],
            explanation=item['explanation'],
            image_url=item['image'],
        )
        
        entry.save()
        
        
def convertDate(date):
    date = date.replace(':', '')
    date = datetime.strptime(date, '%Y-%m-%d')
    return date.strftime('%Y %B %d')


def getTodayPicture(request):
    source = requests.get('https://apod.nasa.gov/apod/archivepix.html').text
    soup = BeautifulSoup(source, 'lxml')
    
    b_tag = soup.find_all('b')[1]
    a_tags = b_tag.find_all('a')
    
    data = scrape_a_tag(a_tags[0])
    return JsonResponse(data, safe=False)
    

def scrape_a_tag(a_tag):
    dictionary = {}

    date = a_tag.find_previous(string=True).strip()
    title = a_tag.text.strip()
    url = f'https://apod.nasa.gov/apod/{a_tag["href"]}'
    image, explanation = getImageAndExplanation(url)

    dictionary['date'] = date
    dictionary['title'] = title
    dictionary['url'] = url
    dictionary['image_url'] = image
    dictionary['explanation'] = explanation

    return dictionary


def getImageAndExplanation(url):
    source = requests.get(url).text
    soup = BeautifulSoup(source, 'lxml')

    p_tags = soup.find_all('p')
    img_tag = soup.find('img')

    try:
        explanation = p_tags[2].get_text()
        img_url = f'https://apod.nasa.gov/apod/{img_tag["src"]}'
    except:
        explanation = None
        img_url = None

    return img_url, explanation


@api_view(['POST'])
def likeImage(request):
    date = json.loads(request.body)['date']
    entry = Gallery.objects.get(date=date)
    
    entry.image_is_liked = True
    entry.image_likes_count += 1
    
    entry.save()
    
    return JsonResponse({'message': 'Image liked successfully!'}, safe=False)
    
    
@api_view(['POST'])
def unlikeImage(request):
    date = json.loads(request.body)['date']
    entry = Gallery.objects.get(date=date)
    
    entry.image_is_liked = False
    entry.image_likes_count -= 1
    
    entry.save()
    
    return JsonResponse({'message': 'Image unliked successfully!'}, safe=False)
