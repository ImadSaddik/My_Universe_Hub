import json
from datetime import datetime

import requests
from django.db.models import Q
from django.http import HttpResponseBadRequest, JsonResponse
from rest_framework.decorators import api_view
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from .apod_scrapper import add_non_existing_images
from .models import Gallery, UserAccount
from .serializers import GallerySerializer


class getArchive(APIView):
    def get(self, request: Request, start_index: int, end_index: int) -> Response:
        entries = Gallery.objects.all()

        sliced_entries = entries[start_index:end_index]
        serializer = GallerySerializer(sliced_entries, many=True)
        return Response(serializer.data)


class getArchiveSize(APIView):
    def get(self, request: Request) -> Response:
        entries = Gallery.objects.all()
        response = {"count": len(entries)}

        return Response(response)


@api_view(["GET"])
def getTodayPicture(request: Request) -> Response | HttpResponseBadRequest:
    todayEntry = Gallery.objects.all()[0]
    today = datetime.now().today().date()
    print(f"Request type: {type(request)}")

    if today != todayEntry.date:
        print("Today's image is not in the database. Adding it now...")

        add_non_existing_images()
        todayEntry = Gallery.objects.all()[0]

        if today != todayEntry.date:
            return HttpResponseBadRequest("Today's image is not available!")

    serializer = GallerySerializer(todayEntry)
    return Response(serializer.data)


@api_view(["POST"])
def likeImage(request: Request) -> JsonResponse | HttpResponseBadRequest:
    data = json.loads(request.body)
    date = data["date"]
    email = data["email"]

    try:
        entry = Gallery.objects.get(date=date)
        user = UserAccount.objects.get(email=email)

        if user not in entry.liked_by_users.all():
            entry.liked_by_users.add(user)
            entry.update_likes()
            entry.save()

        return JsonResponse({"message": "Image liked successfully!"}, safe=False)
    except Exception:
        return HttpResponseBadRequest("Image not found!")


@api_view(["POST"])
def unlikeImage(request: Request) -> JsonResponse | HttpResponseBadRequest:
    data = json.loads(request.body)
    date = data["date"]
    email = data["email"]

    try:
        entry = Gallery.objects.get(date=date)
        user = UserAccount.objects.get(email=email)

        if user in entry.liked_by_users.all():
            entry.liked_by_users.remove(user)
            entry.update_likes()
            entry.save()

        return JsonResponse({"message": "Image unliked successfully!"}, safe=False)
    except Exception:
        return HttpResponseBadRequest("Image not found!")


@api_view(["GET"])
def search(request: Request, query: str, start_index: int, end_index: int) -> Response:
    search_words = query.split(",")
    search_pattern = r"\b(?:" + "|".join(search_words) + r")\b"

    entries = Gallery.objects.filter(Q(explanation__iregex=search_pattern))
    sliced_entries = entries[start_index:end_index]
    serializer = GallerySerializer(sliced_entries, many=True)

    return Response(serializer.data)


@api_view(["GET"])
def searchSize(request: Request, query: str) -> Response:
    search_words = query.split(",")
    search_pattern = r"\b(?:" + "|".join(search_words) + r")\b"

    entries = Gallery.objects.filter(Q(explanation__iregex=search_pattern))
    response = {"count": len(entries)}

    return Response(response)


@api_view(["GET"])
def getSortedArchive(request: Request, start_index: int, end_index: int) -> Response:
    entries = Gallery.objects.order_by("-image_likes_count")
    sliced_entries = entries[start_index:end_index]
    serializer = GallerySerializer(sliced_entries, many=True)

    return Response(serializer.data)


@api_view(["GET"])
def getSortedArchiveSize(request: Request) -> Response:
    entries = Gallery.objects.order_by("-image_likes_count")
    response = {"count": len(entries)}

    return Response(response)


@api_view(["GET"])
def getFavouritesArchive(request: Request, email: str, start_index: int, end_index: int) -> Response:
    user = UserAccount.objects.get(email=email)
    entries = Gallery.objects.filter(liked_by_users=user)

    for entry in entries:
        entry.image_is_liked = True

    sliced_entries = entries[start_index:end_index]
    serializer = GallerySerializer(sliced_entries, many=True)

    return Response(serializer.data)


@api_view(["GET"])
def getFavouritesArchiveSize(request: Request, email: str) -> Response:
    user = UserAccount.objects.get(email=email)
    entries = Gallery.objects.filter(liked_by_users=user)

    response = {"count": len(entries)}

    return Response(response)


@api_view(["POST"])
def resetPassword(request: Request) -> JsonResponse | HttpResponseBadRequest:
    data = json.loads(request.body)
    email = data["email"]
    newPassword = data["newPassword"]

    try:
        user = UserAccount.objects.get(email=email)
        user.set_password(newPassword)
        user.save()
        return JsonResponse({"message": "Password reset successfully!"}, safe=False)

    except UserAccount.DoesNotExist:
        return HttpResponseBadRequest("User not found!")


def apod_health_check(request: Request) -> JsonResponse:
    try:
        response = requests.head("https://apod.nasa.gov/apod/archivepix.html", timeout=5)
        if response.ok:
            return JsonResponse({"status": "up"})
        else:
            return JsonResponse({"status": "down"})
    except requests.exceptions.RequestException:
        return JsonResponse({"status": "down"})
