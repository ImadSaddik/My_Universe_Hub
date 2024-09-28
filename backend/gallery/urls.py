from django.urls import path

from . import views

urlpatterns = [
    path('gallery/<int:start_index>/<int:end_index>/', views.getArchive.as_view(), name='get_archive'),
    path('gallery/count/', views.getArchiveSize.as_view(), name='get_archive_size'),
    path('today/', views.getTodayPicture, name='get_today_picture'),
    path('like_image/', views.likeImage, name='like_image'),
    path('unlike_image/', views.unlikeImage, name='unlike_image'),
    path('search/<str:query>/<int:start_index>/<int:end_index>/', views.search, name='search'),
    path('search/<str:query>/count/', views.searchSize, name='search_size'),
    path('trending/<int:start_index>/<int:end_index>/', views.getSortedArchive, name='get_sorted_archive'),
    path('trending/count/', views.getSortedArchiveSize, name='get_sorted_archive_size'),
    path('favourites/<str:email>/<int:start_index>/<int:end_index>/', views.getFavouritesArchive, name='get_favourites_archive'),
    path('favourites/<str:email>/count/', views.getFavouritesArchiveSize, name='get_favourites_archive_size'),
    path('reset_password/', views.resetPassword, name='reset_password'),
]