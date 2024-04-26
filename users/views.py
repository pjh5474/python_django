from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.exceptions import NotFound
from .models import User
from tweets.serializers import TweetSerializer
from .serializers import UserSerializer, UserDetailSerializer


class Users(APIView):
    def get(self, request):
        users = User.objects.all()
        serializer = UserSerializer(
            users,
            many=True,
        )
        return Response(
            {
                "ok": True,
                "data": serializer.data,
            }
        )


class UserDetail(APIView):
    def get_object(self, user_id):
        try:
            return User.objects.get(id=user_id)
        except User.DoesNotExist:
            raise NotFound

    def get(self, request, user_id):
        userSerializer = UserDetailSerializer(self.get_object(user_id))
        return Response(
            {
                "ok": True,
                "data": {
                    "user": userSerializer.data,
                },
            }
        )


class UserTweets(APIView):
    def get_object(self, user_id):
        try:
            return User.objects.get(id=user_id)
        except User.DoesNotExist:
            raise NotFound

    def get(self, request, user_id):
        userObject = self.get_object(user_id)
        userSerializer = UserSerializer(userObject)
        tweetSerializer = TweetSerializer(
            userObject.tweets,
            many=True,
        )
        return Response(
            {
                "ok": True,
                "data": {
                    "user": userSerializer.data,
                    "tweets": tweetSerializer.data,
                },
            }
        )
