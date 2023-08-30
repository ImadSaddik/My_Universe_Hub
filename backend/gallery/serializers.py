from rest_framework import serializers
from .models import Keyword, Gallery


class GallerySerializer(serializers.ModelSerializer):
    liked_by_users = serializers.StringRelatedField(many=True)
    
    class Meta:
        model = Gallery
        fields = (
            'date',
            'title',
            'explanation',
            'image_url',
            'image_is_liked',
            'image_likes_count',
            'liked_by_users'
        )

