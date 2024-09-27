import os
import json
import requests
import google.generativeai as genai

from bs4 import BeautifulSoup
from datetime import datetime
from dotenv import load_dotenv

from django.db.models import Q
from django.http import JsonResponse, HttpResponseBadRequest

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view

from .models import Gallery, UserAccount
from .serializers import GallerySerializer

load_dotenv()
genai.configure(api_key=os.getenv('GOOGLE_API_KEY'))


class getArchive(APIView):
    def get(self, request, start_index, end_index, format=None):
        entries = Gallery.objects.all()
        
        sliced_entries = entries[start_index:end_index]
        serializer = GallerySerializer(sliced_entries, many=True)
        return Response(serializer.data)
    
    
def addNonExistingImages():
    a_tags = getATags()
    
    for tag in a_tags:
        item = scrape_a_tag(tag)
        if item['image_url'] is None:
            continue
        
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
                authors=item['authors']
            )
            
            entry.save()
        
        
def convertDate(date):
    date = date.replace(':', '')
    return datetime.strptime(date, '%Y %B %d').date()


@api_view(['GET'])
def getTodayPicture(request):
    todayEntry = Gallery.objects.all()[0]
    today = datetime.now().today().date()

    if today != todayEntry.date:
        print('Today\'s image is not in the database. Adding it now...')

        addNonExistingImages()
        todayEntry = Gallery.objects.all()[0]
        
    serializer = GallerySerializer(todayEntry)
    return Response(serializer.data)
    
    
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
    authors = getAuthors(url)

    dictionary['date'] = date
    dictionary['title'] = title
    dictionary['url'] = url
    dictionary['image_url'] = image
    dictionary['explanation'] = explanation
    dictionary['authors'] = authors

    return dictionary


def getImageAndExplanation(url):
    source = requests.get(url).text
    soup = BeautifulSoup(source, 'lxml')

    p_tags = soup.find_all('p')
    img_tag = soup.find('img')
    explanation = p_tags[2].get_text()

    try:
        img_url = f'https://apod.nasa.gov/apod/{img_tag["src"]}'
    except:
        img_url = None

    return img_url, explanation


def getAuthors(url):
    source = requests.get(url).text
    soup = BeautifulSoup(source, 'lxml')

    center_tags = soup.find_all('center')
    credit_center_tag = center_tags[1]
    authors = extractAuthorsWithGemini(credit_center_tag)

    return authors


def extractAuthorsWithGemini(center_tag):
    query = f"""Given the following HTML code snippet, your role is to extract the credit information from the center tag.
The extracted credit information should be returned as a string and separated by a comma to denote multiple authors.
Dont't include prefix text like "Image Credit" or "Illustration Credit".

The HTML code snippet is as follows:
{center_tag}
"""

    model = genai.GenerativeModel('models/gemini-1.5-flash-002')
    response = model.generate_content(query)
    return response.text


@api_view(['POST'])
def likeImage(request):
    data = json.loads(request.body)
    date = data['date']
    email = data['email']

    try:
        entry = Gallery.objects.get(date=date)
        user = UserAccount.objects.get(email=email)

        if user not in entry.liked_by_users.all():
            entry.liked_by_users.add(user)
            entry.update_likes()
            entry.save()

        return JsonResponse({'message': 'Image liked successfully!'}, safe=False)
    except Exception:
        return HttpResponseBadRequest('Image not found!')
    
    
@api_view(['POST'])
def unlikeImage(request):
    data = json.loads(request.body)
    date = data['date']
    email = data['email']

    try:
        entry = Gallery.objects.get(date=date)
        user = UserAccount.objects.get(email=email)

        if user in entry.liked_by_users.all():
            entry.liked_by_users.remove(user)
            entry.update_likes()
            entry.save()

        return JsonResponse({'message': 'Image unliked successfully!'}, safe=False)
    except Exception:
        return HttpResponseBadRequest('Image not found!')


@api_view(['GET'])
def search(request, query, start_index, end_index):
    search_words = query.split(',')
    search_pattern = r'\b(?:' + '|'.join(search_words) + r')\b'
    
    entries = Gallery.objects.filter(Q(explanation__iregex=search_pattern))
    sliced_entries = entries[start_index:end_index]
    serializer = GallerySerializer(sliced_entries, many=True)
    
    return Response(serializer.data)


@api_view(['GET'])
def getSortedArchive(request, start_index, end_index):
    entries = Gallery.objects.order_by('-image_likes_count')
    sliced_entries = entries[start_index:end_index]
    serializer = GallerySerializer(sliced_entries, many=True)
    
    return Response(serializer.data)


@api_view(['GET'])
def getFavouritesArchive(request, email):
    user = UserAccount.objects.get(email=email)
    entries = Gallery.objects.filter(liked_by_users=user)
    
    for entry in entries:
        entry.image_is_liked = True
    
    serializer = GallerySerializer(entries, many=True)
    
    return Response(serializer.data)


@api_view(['POST'])
def resetPassword(request):
    data = json.loads(request.body)
    email = data['email']
    newPassword = data['newPassword']
    
    try:    
        user = UserAccount.objects.get(email=email)
        user.set_password(newPassword)
        user.save()
        return JsonResponse({'message': 'Password reset successfully!'}, safe=False)
    
    except UserAccount.DoesNotExist:
        return HttpResponseBadRequest('User not found!')
