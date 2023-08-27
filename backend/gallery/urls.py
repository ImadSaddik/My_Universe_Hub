from django.urls import path

from . import views

urlpatterns = [
    path('gallery/', views.getArchive.as_view()),
    path('today/', views.getTodayPicture),
]