from django.urls import path

from . import views

urlpatterns = [
    path('gallery/<int:start_index>/<int:end_index>/', views.getArchive.as_view(), name='get_archive'),
    path('today/', views.getTodayPicture, name='get_today_picture'),
    path('like_image/', views.likeImage, name='like_image'),
    path('unlike_image/', views.unlikeImage, name='unlike_image'),
    path('search/<str:query>/<int:start_index>/<int:end_index>/', views.search, name='search'),
    path('trending/<int:start_index>/<int:end_index>/', views.getSortedArchive, name='get_sorted_archive'),
    path('favourites/<str:email>/', views.getFavouritesArchive, name='get_favourites_archive'),
    path('reset_password/', views.resetPassword, name='reset_password'),
]