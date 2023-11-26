from django.conf import settings
from django.contrib.auth import authenticate, login, logout
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from ..serializers import UserSerializer
from ..helpers import get_discord_user


class SignUpView(APIView):
    """View to Sign Up a new account on the API."""
    BASE_URL = "https://discord.com/api/v10"

    def get(self, request: Request):
        """GET method to handle Discord codes and requests."""
        if request.GET.get("code", 0):
            try:
                code = request.GET['code']
                response = get_discord_user(code, self.BASE_URL)
                json_info = {
                    'username': response['username'],
                    'password': response['id']
                }
                serializer = UserSerializer(data=json_info)
                if serializer.is_valid():
                    user = serializer.create(serializer.validated_data)
                    user.save()
                return Response({"info": "User created"}, status=201)
            except KeyError:
                return Response({"info": "Service down."}, status=500)
        return Response({"info": "Bad request"}, status=400)

    def post(self, _):
        """POST Method returns discord URI to log using Discord OAuth2"""
        content = {
            "discord_uri":
                self.BASE_URL +
                f"/oauth2/authorize?client_id={settings.DISCORD_CLIENT_ID}&" +
                "redirect_uri=http%3A%2F%2Flocalhost%3A8000%2Fapi%2Fsign-up" +
                "&response_type=code&scope=identify"
        }
        return Response(content)


class SignInView(APIView):
    """View for SignIn methods."""

    def get(self, request: Request):
        """GET Method return the current user and it's authentication."""
        content = {
            "user": str(request.user),
            "auth": str(request.auth),
        }
        return Response(content, status=200)

    def post(self, request: Request):
        """POST method log in the user returning it's Session id."""
        content = {
            "username": str(request.data.get("username", 0)),
            "password": str(request.data.get("password", 0)),
        }
        user = authenticate(request,
                            username=content["username"],
                            password=content["password"])
        if user:
            login(request, user)
            return Response({"info": "Logged in"}, status=200)
        return Response({"info": "Invalid user"}, status=404)


class SignOutView(APIView):
    """View to Sign Out a user logged in."""

    def post(self, request: Request):
        """Post method to log out the user."""
        if request.user.is_authenticated:
            logout(request)
            return Response({"info": "Logged out correctly."}, status=200)
        return Response({"info": "User not found."}, status=400)
