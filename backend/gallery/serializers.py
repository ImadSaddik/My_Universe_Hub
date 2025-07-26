from django.contrib.auth import get_user_model
from djoser.serializers import UserCreateSerializer as DjoserUserCreateSerializer
from rest_framework import serializers

from .models import Gallery


class UserCreateSerializer(DjoserUserCreateSerializer):
    class Meta(DjoserUserCreateSerializer.Meta):
        model = get_user_model()
        fields = ("id", "email", "name", "password")


class GallerySerializer(serializers.ModelSerializer):
    liked_by_users = serializers.StringRelatedField(many=True)
    comments = serializers.StringRelatedField(many=True)

    class Meta:
        model = Gallery
        fields = (
            "date",
            "title",
            "explanation",
            "image_url",
            "image_is_liked",
            "image_likes_count",
            "liked_by_users",
            "comments",
            "authors",
        )
