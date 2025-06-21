import json
import logging
from datetime import datetime

import requests
from django.db.models import Q
from django.http import HttpResponseBadRequest, JsonResponse
from rest_framework.decorators import api_view
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from .apod_scrapper import add_non_existing_images
from .models import Gallery, UserAccount, UserVisit
from .serializers import GallerySerializer

logger = logging.getLogger(__name__)


class getArchive(APIView):
    def get(self, request: Request, start_index: int, end_index: int) -> Response:
        try:
            entries = Gallery.objects.all()
            sliced_entries = entries[start_index:end_index]
            serializer = GallerySerializer(sliced_entries, many=True)
            logger.info(f"Fetched {len(sliced_entries)} entries from archive [{start_index}:{end_index}]")
            return Response(serializer.data)
        except Exception as e:
            logger.error(f"Error in getArchive: {e}")
            return HttpResponseBadRequest("An error occurred while fetching the archive.")


class getArchiveSize(APIView):
    def get(self, request: Request) -> Response:
        try:
            entries = Gallery.objects.all()
            response = {"count": entries.count()}
            logger.info(f"Archive size: {response['count']}")
            return Response(response)
        except Exception as e:
            logger.error(f"Error in getArchiveSize: {e}")
            return HttpResponseBadRequest("An error occurred while fetching the archive size.")


@api_view(["GET"])
def getTodayPicture(request: Request) -> Response | HttpResponseBadRequest:
    logger.info("Fetching today's image from the database...")

    try:
        todayEntry = Gallery.objects.all().first()
        today = datetime.now().today().date()

        if todayEntry and today != todayEntry.date:
            logger.info("Today's image is not in the database. Adding it now...")

            add_non_existing_images()
            todayEntry = Gallery.objects.all().first()

            if todayEntry and today != todayEntry.date:
                logger.warning("Today's image is still not available after adding new images.")
                return HttpResponseBadRequest("Today's image is not available!")

        serializer = GallerySerializer(todayEntry)
        logger.info("Today's image fetched successfully.")
        return Response(serializer.data)
    except Gallery.DoesNotExist:
        logger.error("No images found in the database.")
        return HttpResponseBadRequest("No images found in the database!")
    except Exception as e:
        logger.error(f"Error fetching today's image: {e}")
        return HttpResponseBadRequest("An error occurred while fetching today's image!")


@api_view(["POST"])
def likeImage(request: Request) -> JsonResponse | HttpResponseBadRequest:
    logger.info("Processing likeImage request...")

    try:
        data = json.loads(request.body)
        date = data["date"]
        email = data["email"]

        entry = Gallery.objects.get(date=date)
        user = UserAccount.objects.get(email=email)

        if user not in entry.liked_by_users.all():
            entry.liked_by_users.add(user)
            entry.update_likes()
            entry.save()

        logger.info(f"Image liked by user: {user.email}")
        return JsonResponse({"message": "Image liked successfully!"}, safe=False)
    except json.JSONDecodeError as e:
        logger.error(f"Invalid JSON in likeImage: {e}")
        return HttpResponseBadRequest("Invalid JSON!")
    except Exception as e:
        logger.error(f"Error in likeImage: {e}")
        return HttpResponseBadRequest("Something went wrong while liking the image!")


@api_view(["POST"])
def unlikeImage(request: Request) -> JsonResponse | HttpResponseBadRequest:
    logger.info("Processing unlikeImage request...")

    try:
        data = json.loads(request.body)
        date = data["date"]
        email = data["email"]

        entry = Gallery.objects.get(date=date)
        user = UserAccount.objects.get(email=email)

        if user in entry.liked_by_users.all():
            entry.liked_by_users.remove(user)
            entry.update_likes()
            entry.save()

        logger.info(f"Image unliked by user: {user.email}")
        return JsonResponse({"message": "Image unliked successfully!"}, safe=False)
    except json.JSONDecodeError as e:
        logger.error(f"Invalid JSON in unlikeImage: {e}")
        return HttpResponseBadRequest("Invalid JSON!")
    except Exception as e:
        logger.error(f"Error in unlikeImage: {e}")
        return HttpResponseBadRequest("Something went wrong while unliking the image!")


@api_view(["GET"])
def search(request: Request, query: str, start_index: int, end_index: int) -> Response:
    logger.info(f"Searching for query: {query} from index {start_index} to {end_index}")

    try:
        search_words = query.split(",")
        search_pattern = r"\b(?:" + "|".join(search_words) + r")\b"

        entries = Gallery.objects.filter(Q(explanation__iregex=search_pattern))
        sliced_entries = entries[start_index:end_index]
        serializer = GallerySerializer(sliced_entries, many=True)

        logger.info(f"Found {len(sliced_entries)} entries for query: {query}")
        return Response(serializer.data)
    except Exception as e:
        logger.error(f"Error in search: {e}")
        return HttpResponseBadRequest("An error occurred while fetching the search results!")


@api_view(["GET"])
def searchSize(request: Request, query: str) -> Response:
    logger.info(f"Searching for size of query: {query}")

    try:
        search_words = query.split(",")
        search_pattern = r"\b(?:" + "|".join(search_words) + r")\b"

        entries = Gallery.objects.filter(Q(explanation__iregex=search_pattern))
        response = {"count": entries.count()}

        logger.info(f"Found {response['count']} entries for size query: {query}")
        return Response(response)
    except Exception as e:
        logger.error(f"Error in searchSize: {e}")
        return HttpResponseBadRequest("An error occurred while fetching the search size!")


@api_view(["GET"])
def getSortedArchive(request: Request, start_index: int, end_index: int) -> Response:
    logger.info(f"Fetching sorted archive from index {start_index} to {end_index}")

    try:
        entries = Gallery.objects.order_by("-image_likes_count")
        sliced_entries = entries[start_index:end_index]
        serializer = GallerySerializer(sliced_entries, many=True)

        logger.info(f"Fetched {len(sliced_entries)} entries from sorted archive.")
        return Response(serializer.data)
    except Exception as e:
        logger.error(f"Error in getSortedArchive: {e}")
        return HttpResponseBadRequest("An error occurred while fetching the sorted archive!")


@api_view(["GET"])
def getSortedArchiveSize(request: Request) -> Response:
    logger.info("Fetching size of sorted archive.")

    try:
        entries = Gallery.objects.order_by("-image_likes_count")
        response = {"count": entries.count()}

        logger.info(f"Sorted archive size: {response['count']}")
        return Response(response)
    except Exception as e:
        logger.error(f"Error in getSortedArchiveSize: {e}")
        return HttpResponseBadRequest("An error occurred while fetching the sorted archive size!")


@api_view(["GET"])
def getFavouritesArchive(request: Request, email: str, start_index: int, end_index: int) -> Response:
    logger.info(f"Fetching favourites archive for user: {email} from index {start_index} to {end_index}")

    try:
        user = UserAccount.objects.get(email=email)
        entries = Gallery.objects.filter(liked_by_users=user)

        for entry in entries:
            entry.image_is_liked = True

        sliced_entries = entries[start_index:end_index]
        serializer = GallerySerializer(sliced_entries, many=True)

        logger.info(f"Fetched {len(sliced_entries)} entries from favourites archive for user: {email}")
        return Response(serializer.data)
    except UserAccount.DoesNotExist:
        logger.error(f"User not found in getFavouritesArchive: {email}")
        return HttpResponseBadRequest("User not found!")
    except Exception as e:
        logger.error(f"Error in getFavouritesArchive: {e}")
        return HttpResponseBadRequest("An error occurred!")


@api_view(["GET"])
def getFavouritesArchiveSize(request: Request, email: str) -> Response:
    logger.info(f"Fetching size of favourites archive for user: {email}")

    try:
        user = UserAccount.objects.get(email=email)
        entries = Gallery.objects.filter(liked_by_users=user)

        response = {"count": entries.count()}
        logger.info(f"Fetched size of favourites archive for user: {email}: {response['count']}")
        return Response(response)
    except UserAccount.DoesNotExist:
        logger.error(f"User not found in getFavouritesArchiveSize: {email}")
        return HttpResponseBadRequest("User not found!")
    except Exception as e:
        logger.error(f"Error in getFavouritesArchiveSize: {e}")
        return HttpResponseBadRequest("An error occurred!")


@api_view(["POST"])
def resetPassword(request: Request) -> JsonResponse | HttpResponseBadRequest:
    logger.info("Processing resetPassword request...")

    try:
        data = json.loads(request.body)
        email = data["email"]
        newPassword = data["newPassword"]

        user = UserAccount.objects.get(email=email)
        user.set_password(newPassword)
        user.save()
        logger.info(f"Password reset successfully for user: {email}")
        return JsonResponse({"message": "Password reset successfully!"}, safe=False)
    except json.JSONDecodeError as e:
        logger.error(f"Invalid JSON in resetPassword: {e}")
        return HttpResponseBadRequest("Invalid JSON!")
    except UserAccount.DoesNotExist as e:
        logger.error(f"User not found in resetPassword: {e}")
        return HttpResponseBadRequest("User not found!")
    except Exception as e:
        logger.error(f"Error in resetPassword: {e}")
        return HttpResponseBadRequest("An error occurred!")


@api_view(["GET"])
def apod_health_check(request: Request) -> JsonResponse:
    logger.info("Performing health check for APOD service...")

    try:
        response = requests.head("https://apod.nasa.gov/apod/archivepix.html", timeout=5)
        if response.ok:
            logger.info("APOD service is up.")
            return JsonResponse({"status": "up"})
        else:
            logger.warning("APOD service is down or unreachable.")
            return JsonResponse({"status": "down"})
    except requests.exceptions.RequestException:
        logger.error("APOD service is down or unreachable.")
        return JsonResponse({"status": "down"})


@api_view(["POST"])
def log_user_visit(request: Request) -> JsonResponse | HttpResponseBadRequest:
    logger.info("Logging user visit...")

    try:
        data = json.loads(request.body)
        email = data.get("email")
        if not email:
            logger.error("Email is required in log_user_visit.")
            return HttpResponseBadRequest("Email is required.")

        user = UserAccount.objects.get(email=email)
        ip_address = request.META.get("HTTP_X_FORWARDED_FOR")
        user_agent = request.META.get("HTTP_USER_AGENT", "")[:255]

        UserVisit.objects.create(
            user=user,
            ip_address=ip_address,
            user_agent=user_agent,
        )
        logger.info(f"User visit logged: {email}, {ip_address}, {user_agent}")
        return JsonResponse({"message": "Visit logged."})
    except json.JSONDecodeError as e:
        logger.error(f"Invalid JSON in log_user_visit: {e}")
        return HttpResponseBadRequest("Invalid JSON.")
    except UserAccount.DoesNotExist as e:
        logger.error(f"User not found in log_user_visit: {e}")
        return HttpResponseBadRequest("User not found.")
    except Exception as e:
        logger.error(f"Error in log_user_visit: {e}")
        return HttpResponseBadRequest(str(e))
