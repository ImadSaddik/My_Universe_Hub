from django.urls import path

from . import views

urlpatterns = [
    path('gallery/', views.getArchive.as_view(), name='get_archive'),
    path('today/', views.getTodayPicture, name='get_today_picture'),
    path('like_image/', views.likeImage, name='like_image'),
    path('unlike_image/', views.unlikeImage, name='unlike_image'),
    path('search/<str:query>/', views.search, name='search'),
    path('trending/', views.getSortedArchive, name='get_sorted_archive'),
    path('favourites/<str:username>/', views.getFavouritesArchive, name='get_favourites_archive'),
]