import os
from django.conf import settings
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.renderers import JSONRenderer
from ..serializers import ImageSerializer, VideoSerializer, AudioSerializer, MediaSerializer
from ..models import MediaFile, Image, Video, Audio


class MediaView(APIView):
    """
    APIView to be extended from MediaFile Files.
    """
    model = MediaFile
    serializer = MediaSerializer

    def get(self, request: Request, id: int = 0):
        """Returns a set or unique media file associated with the user or/with id provided."""
        if request.user.is_authenticated:
            if id:
                try:
                    media = self.model.objects.get(id=id)
                    serializer = self.serializer(media)
                    serialized = JSONRenderer().render(serializer.data)
                    return Response(data=serialized, status=200)
                except Exception as ex:
                    error_message = str(ex)
            else:
                media = self.model.objects.filter(author=request.user.username)
                serialized = JSONRenderer().render(media.values())
                return Response(data=serialized, status=200)
        return Response({"result": error_message}, status=400)

    def post(self, request: Request, *_):
        """Uploads a media file corresponding with a user account"""
        if request.user.is_authenticated:
            serializer = self.serializer(data=request.data)
            if serializer.is_valid():
                print("Valid format.")
                serializer.create(serializer.validated_data, request.user)
                serialized = JSONRenderer().render(serializer.data)
                return Response(data=serialized, status=201)
        return Response({"result": "Malformed Request"}, status=400)

    def put(self, request: Request, id: int = 0):
        """Replaces an existing media file with a new one."""
        if request.user.is_authenticated:
            serializer = self.serializer(data=request.data)
            if serializer.is_valid():
                try:
                    file = self.model.objects.get(id=id)
                    media_path = os.path.join(
                        settings.MEDIA_ROOT, str(file.file))
                    os.remove(media_path)
                    file.file = serializer.validated_data['file']
                    file.save()
                    return Response({"result": f"Replaced media {id} "})
                except Exception as ex:
                    error_message = str(ex)
        return Response({"result": f"{error_message}"}, status=404)

    def delete(self, request: Request, id: int = 0):
        """Deletes an existing media file on a user account."""
        if request.user.is_authenticated:
            try:
                file = self.model.objects.get(id=id)
                media_path = os.path.join(settings.MEDIA_ROOT, str(file.file))
                file.delete()
                os.remove(media_path)
                return Response({"result": f"Deleted media {id} "})
            except Exception as ex:
                error_message = str(ex)
        return Response({"result": f"{error_message}"}, status=404)


class ImageView(MediaView):
    """ Image View inherited from MediaView to manage all image request """
    model = Image
    serializer = ImageSerializer


class AudioView(MediaView):
    """ Audio View inherited from MediaView to manage all image request """
    model = Audio
    serializer = AudioSerializer


class VideoView(MediaView):
    """ Video View inherited from MediaView to manage all image request """
    model = Video
    serializer = VideoSerializer
