from django.contrib.auth import authenticate, login, logout
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .models import User
from tweets.serializers import TweetSerializer
from .serializers import UserSerializer, UserDetailSerializer


# GET / POST
class Users(APIView):
    def get(self, request):
        users = User.objects.all()
        userSerializer = UserSerializer(
            users,
            many=True,
        )
        return Response(
            {
                "ok": True,
                "data": userSerializer.data,
            },
            status=status.HTTP_200_OK,
        )

    def post(self, request):
        password = request.data.get("password")
        if not password:
            return Response(
                {
                    "ok": False,
                    "error": "You need to send password",
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        userSerializer = UserDetailSerializer(data=request.data)

        if userSerializer.is_valid():
            user = userSerializer.save()
            user.set_password(password)
            user.save()
            userSerializer = UserDetailSerializer(user)
            return Response(
                userSerializer.data,
                status=status.HTTP_201_CREATED,
            )
        else:
            return Response(
                userSerializer.errors,
                status=status.HTTP_400_BAD_REQUEST,
            )


# GET
class UserDetail(APIView):
    def get_object(self, user_id):
        try:
            return User.objects.get(id=user_id)
        except User.DoesNotExist:
            return "NotFound"

    def get(self, request, user_id):
        user = self.get_object(user_id)
        if user == "NotFound":
            return Response(
                {
                    "ok": False,
                    "error": f"No user with id : {user_id}",
                },
                status=status.HTTP_404_NOT_FOUND,
            )

        userSerializer = UserDetailSerializer(user)
        return Response(
            {
                "ok": True,
                "data": {
                    "user": userSerializer.data,
                },
            },
            status=status.HTTP_200_OK,
        )

    def put(self, request, user_id):
        userSerializer = UserDetailSerializer(
            self.get_object(user_id),
            data=request.data,
            partial=True,
        )
        if userSerializer.is_valid():
            user = userSerializer.save()
            userSerializer = UserDetailSerializer(user)
            return Response(
                userSerializer.data,
                status=status.HTTP_200_OK,
            )
        else:
            return Response(
                userSerializer.errors,
                status=status.HTTP_400_BAD_REQUEST,
            )


# GET
class UserTweets(APIView):
    def get_object(self, user_id):
        try:
            return User.objects.get(id=user_id)
        except User.DoesNotExist:
            return "NotFound"

    def get(self, request, user_id):
        user = self.get_object(user_id)
        if user == "NotFound":
            return Response(
                {
                    "ok": False,
                    "error": f"No user with id : {user_id}",
                },
                status=status.HTTP_404_NOT_FOUND,
            )

        userSerializer = UserSerializer(user)
        tweetSerializer = TweetSerializer(
            user.tweets,
            many=True,
        )
        return Response(
            {
                "ok": True,
                "data": {
                    "user": userSerializer.data,
                    "tweets": tweetSerializer.data,
                },
            },
            status=status.HTTP_200_OK,
        )


# PUT /api/v1/users/password: Change password of logged in user.
class ChangePassword(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response(
            {
                "put method input example": {
                    "old_password": "old",
                    "new_password": "new",
                    "new_password_check": "new",
                }
            }
        )

    def put(self, request):
        user = request.user
        old_password = request.data.get("old_password")
        new_password = request.data.get("new_password")
        new_password_check = request.data.get("new_password_check")

        if not old_password or not new_password or not new_password_check:
            return Response(
                {
                    "ok": False,
                    "error": "You need to send 3 values. 1) old_password,  2) new_password, 3) new_password_check",
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        if old_password == new_password:
            return Response(
                {
                    "ok": False,
                    "error": "new_password is equal to old_password",
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        if new_password != new_password_check:
            return Response(
                {
                    "ok": False,
                    "error": "new_password is not equal to new_password_check",
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        if user.check_password(old_password):
            user.set_password(new_password)
            user.save()
            return Response(
                {
                    "ok": True,
                    "error": "Your password is updated successfully",
                },
                status=status.HTTP_200_OK,
            )
        else:
            return Response(
                {
                    "ok": False,
                    "error": "Check your old password",
                },
                status=status.HTTP_400_BAD_REQUEST,
            )


# POST /api/v1/users/login: Log user in
class Login(APIView):
    def get(self, request):
        return Response(
            {
                "post method input example": {
                    "username": "username",
                    "password": "password",
                }
            }
        )

    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")

        if not username or not password:
            return Response(
                {
                    "ok": False,
                    "error": "You need to send 2 values. 1) username,  2) password",
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        user = authenticate(
            request,
            username=username,
            password=password,
        )
        if user:
            login(request, user)
            return Response(
                {
                    "ok": True,
                    "data": f"Welcome, {username}",
                },
                status=status.HTTP_200_OK,
            )
        else:
            return Response(
                {"ok": False, "error": "Check username and password are correct"},
                status=status.HTTP_400_BAD_REQUEST,
            )


# POST /api/v1/users/logout: Log user out
class Logout(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request):
        username = request.user
        logout(request)
        return Response(
            {
                "ok": True,
                "data": f"Bye bye, {username}",
            },
            status=status.HTTP_200_OK,
        )
