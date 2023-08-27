from django.urls import path

from . import views

urlpatterns = [
    path('gallery/', views.getArchive.as_view()),
    path('today/', views.getTodayPicture),
    path('like_image/', views.likeImage),
    path('unlike_image/', views.unlikeImage),
]