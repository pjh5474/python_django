from rest_framework import serializers


class TweetUserSerializer(serializers.Serializer):
    username = serializers.CharField()


class TweetLikeSerializer(serializers.Serializer):
    user = TweetUserSerializer()
    created_at = serializers.DateTimeField()


class TweetSerializer(serializers.Serializer):
    payload = serializers.CharField(
        required=True,
        max_length=180,
    )
    user = TweetUserSerializer()
    likes = TweetLikeSerializer(many=True)
    created_at = serializers.DateTimeField()
    updated_at = serializers.DateTimeField()


class UserTweetSerializer(serializers.Serializer):
    payload = serializers.CharField(
        required=True,
        max_length=180,
    )
    likes = TweetLikeSerializer(many=True)
    created_at = serializers.DateTimeField()
    updated_at = serializers.DateTimeField()
