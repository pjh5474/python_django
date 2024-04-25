from rest_framework import serializers
from tweets.serializers import UserTweetSerializer


class UserTweetsSerializer(serializers.Serializer):
    username = serializers.CharField()
    tweets = UserTweetSerializer(
        many=True,
    )
