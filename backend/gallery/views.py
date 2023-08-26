import pickle

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
