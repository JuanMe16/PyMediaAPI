import os
from django.db import models
from django.contrib.auth.models import User

"""
Functions to returns path location for django to save media files.
"""


def locate_image(instance, filename: str):
    return os.path.join(f'images/{instance.author}/', filename)


def locate_audio(instance, filename: str):
    return os.path.join(f'audio/{instance.author}/', filename)


def locate_video(instance, filename: str):
    return os.path.join(f'video/{instance.author}/', filename)


class MediaFile(models.Model):
    """Abstract Super Class for MediaFiles"""
    title = models.CharField(max_length=50)
    description = models.TextField(default='Empty.', blank=True, null=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, to_field="username")
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True
        ordering = ["date"]

    def __str__(self):
        return str(self.title)


class Image(MediaFile):
    """Subclass for Images"""
    file = models.ImageField(upload_to=locate_image)

    class Meta(MediaFile.Meta):
        db_table = "images"


class Audio(MediaFile):
    """Subclass for Audio"""
    file = models.FileField(upload_to=locate_audio)

    class Meta(MediaFile.Meta):
        db_table = 'audios'


class Video(MediaFile):
    """Subclass for Video"""
    file = models.FileField(upload_to=locate_video)

    class Meta(MediaFile.Meta):
        db_table = 'videos'
