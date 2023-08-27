from django.urls import path

from . import views

urlpatterns = [
    path('gallery/', views.getArchive),
    path('today/', views.getTodayPicture),
]