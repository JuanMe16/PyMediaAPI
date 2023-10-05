from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Image, Video, Audio

class UserSerializer(serializers.Serializer):
    """Serializer to create an User Entity."""
    username = serializers.CharField(max_length=70)
    password = serializers.CharField(min_length=8)

    def create(self, validated_data):
        """Create a new user and set it's password."""
        user = User.objects.create(username=validated_data['username'])
        user.set_password(validated_data['password'])
        return user
    
class MediaSerializer(serializers.Serializer):
    """Abstract Serializer to inherit in Image, Video and Audio."""
    title = serializers.CharField(max_length=50)
    description = serializers.CharField()
    file = serializers.FileField()

class ImageSerializer(MediaSerializer):
    """Image Serializer, Save image type files."""

    def create(self, validated_data, user):
        """Creates a new image and saves it in db."""
        image = Image.objects.create(**validated_data, author=user)
        image.save()
        return image
    
class VideoSerializer(MediaSerializer):
    """Video Serializer, Save video type files."""

    def create(self, validated_data, user):
        """Creates a new image and saves it in db."""
        video = Video.objects.create(**validated_data, author=user)
        video.save()
        return video
    
class AudioSerializer(MediaSerializer):
    """Audio Serializer, Save audio type files."""

    def create(self, validated_data, user):
        """Creates a new audio and saves it in db."""
        audio = Audio.objects.create(**validated_data, author=user)
        audio.save()
        return audio
