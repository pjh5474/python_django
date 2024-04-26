from rest_framework import serializers
from .models import Tweet, Like
from users.serializers import UserSerializer


class TweetSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Tweet
        fields = (
            "payload",
            "user",
            "like_count",
            "created_at",
        )


class LikeSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Like
        fields = (
            "user",
            "created_at",
        )


class TweetDetailSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    likes = LikeSerializer(
        many=True,
        read_only=True,
    )

    class Meta:
        model = Tweet
        fields = "__all__"
