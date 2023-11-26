from django.urls import path
from ..views import auth

urlpatterns = [
    path('sign-in/', auth.SignInView.as_view()),
    path('sign-up/', auth.SignUpView.as_view()),
    path('sign-out/', auth.SignOutView.as_view())
]