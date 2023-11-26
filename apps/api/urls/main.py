from django.urls import path, include


urlpatterns = [
    path('auth/', include("apps.api.urls.users")),
    path('media/', include("apps.api.urls.media")),
]