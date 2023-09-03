import json
import datetime
import requests
from bs4 import BeautifulSoup
from datetime import datetime

from django.db.models import Q
from django.http import JsonResponse, HttpResponseBadRequest, HttpRequest
from django.contrib.auth.models import User

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view

from .models import Gallery
from .serializers import GallerySerializer


class getArchive(APIView):
    def get(self, request, format=None):
        entries = Gallery.objects.all()
        
        today = datetime.now().today().date()
        if today != entries[0].date:
            addNonExistingImages()
        
        serializer = GallerySerializer(entries, many=True)
        return Response(serializer.data)
    
    
def addNonExistingImages():
    a_tags = getATags()
    
    for tag in a_tags:
        item = scrape_a_tag(tag)
        item['date'] = convertDate(item['date'])
        
        try:
            Gallery.objects.get(date=item['date'])
            print(f"{item['date']} is already in the database.")
            break
        except:
            print(f"{item['date']} is not in the database.")
            entry = Gallery.objects.create(
                date=item['date'],
                title=item['title'],
                explanation=item['explanation'],
                image_url=item['image_url'],
            )
            
            entry.save()
        
        
def convertDate(date):
    date = date.replace(':', '')
    return datetime.strptime(date, '%Y %B %d').date()


@api_view(['GET'])
def getTodayPicture(request):
    try:
        todayEntry = Gallery.objects.all()[0]
        today = datetime.now().today().date()
        
        if today == todayEntry.date:
            serializer = GallerySerializer(todayEntry)
            return Response(serializer.data)
        else:
            print('Today\'s image is not in the database. Adding it now...')
            return getLatestPicture()
    except:
        print('Today\'s image is not in the database. Adding it now...')
        return getLatestPicture()
    
    
def getLatestPicture():
    a_tags = getATags()
    
    data = scrape_a_tag(a_tags[0])
    return JsonResponse(data, safe=False)


def getATags():
    source = requests.get('https://apod.nasa.gov/apod/archivepix.html').text
    soup = BeautifulSoup(source, 'lxml')
    
    b_tag = soup.find_all('b')[1]
    return b_tag.find_all('a')
    

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
    data = json.loads(request.body)
    date = data['date']
    username = data['username']
    
    try:
        entry = Gallery.objects.get(date=date)
        user = User.objects.get(username=username)
        
        if user not in entry.liked_by_users.all():
            entry.liked_by_users.add(user)
            entry.update_likes()
            entry.save()
        
        return JsonResponse({'message': 'Image liked successfully!'}, safe=False)
    except:
        return HttpResponseBadRequest('Image not found!')
    
    
@api_view(['POST'])
def unlikeImage(request):
    data = json.loads(request.body)
    date = data['date']
    username = data['username']
    
    try:
        entry = Gallery.objects.get(date=date)
        user = User.objects.get(username=username)
        
        if user in entry.liked_by_users.all():
            entry.liked_by_users.remove(user)
            entry.update_likes()
            entry.save()
        
        return JsonResponse({'message': 'Image unliked successfully!'}, safe=False)
    except:
        return HttpResponseBadRequest('Image not found!')


@api_view(['GET'])
def search(request, query):
    entries = Gallery.objects.filter(Q(explanation__icontains=query))
    serializer = GallerySerializer(entries, many=True)
    
    return Response(serializer.data)


@api_view(['GET'])
def getSortedArchive(request):
    entries = Gallery.objects.order_by('-image_likes_count')
    serializer = GallerySerializer(entries, many=True)
    
    return Response(serializer.data)


@api_view(['GET'])
def getFavouritesArchive(request, username):
    user = User.objects.get(username=username)
    entries = Gallery.objects.filter(liked_by_users=user)
    
    for entry in entries:
        entry.image_is_liked = True
    
    serializer = GallerySerializer(entries, many=True)
    
    return Response(serializer.data)
