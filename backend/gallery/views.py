import pickle
import requests
from bs4 import BeautifulSoup
import concurrent.futures

from django.http import JsonResponse

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view


def getArchive(request):
    with open('/home/imad/Projects/APOD/website/backend/gallery/archive.pickle', 'rb') as f:
        data = pickle.load(f)
        
    data_with_no_null_urls = []
    for item in data:
        if item['image'] != None:
            data_with_no_null_urls.append(item)
        
    return JsonResponse(data_with_no_null_urls, safe=False)


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
    dictionary['image'] = image
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
