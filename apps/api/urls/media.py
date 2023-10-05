from django.urls import path
from ..views import media

urlpatterns = [
    path('image/', media.ImageView.as_view()),
    path('image/<int:id>', media.ImageView.as_view()),
    path('audio/', media.AudioView.as_view()),
    path('audio/<int:id>', media.AudioView.as_view()),
    path('video/', media.VideoView.as_view()),
    path('video/<int:id>', media.VideoView.as_view())
]