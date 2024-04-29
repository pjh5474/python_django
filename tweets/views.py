from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from .serializers import TweetSerializer, TweetDetailSerializer
from .models import Tweet as TweetModel


# Get / Post
class Tweets(APIView):
    def get(self, request):
        tweets = TweetModel.objects.all()
        serializer = TweetSerializer(
            tweets,
            many=True,
        )
        return Response(
            {
                "ok": True,
                "data": serializer.data,
            },
            status=status.HTTP_200_OK,
        )

    def post(self, request):
        if request.user.is_authenticated:
            tweetData = request.data
            serializer = TweetDetailSerializer(data=tweetData)
            if serializer.is_valid():
                tweet = serializer.save(user=request.user)
                serializer = TweetDetailSerializer(tweet)
                return Response(
                    {
                        "ok": True,
                        "data": serializer.data,
                    },
                    status=status.HTTP_200_OK,
                )
            else:
                return Response(
                    {
                        "ok": False,
                        "error": serializer.errors,
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )
        else:
            return Response(
                {"ok": False, "error": "Please login first"},
                status=status.HTTP_401_UNAUTHORIZED,
            )


# Get / Put / Delete
class TweetDetail(APIView):
    def get_object(self, tweet_id):
        try:
            return TweetModel.objects.get(id=tweet_id)
        except TweetModel.DoesNotExist:
            return "NotFound"

    def get(self, request, tweet_id):
        tweet = self.get_object(tweet_id)
        if tweet == "NotFound":
            return Response(
                {
                    "ok": False,
                    "error": f"No tweet with id : {tweet_id}",
                },
                status=status.HTTP_404_NOT_FOUND,
            )

        serializer = TweetDetailSerializer(tweet)
        return Response(
            {
                "ok": True,
                "data": serializer.data,
            },
            status=status.HTTP_200_OK,
        )

    def put(self, request, tweet_id):
        tweet = self.get_object(tweet_id)
        if tweet == "NotFound":
            return Response(
                {
                    "ok": False,
                    "error": f"No tweet with id : {tweet_id}",
                },
                status=status.HTTP_404_NOT_FOUND,
            )

        if not request.user.is_authenticated:
            return Response(
                {
                    "ok": False,
                    "error": "Please login first",
                },
                status=status.HTTP_401_UNAUTHORIZED,
            )

        if tweet.user != request.user:
            return Response(
                {
                    "ok": False,
                    "error": "You can only edit your own tweets",
                },
                status=status.HTTP_403_FORBIDDEN,
            )

        tweetSerializer = TweetDetailSerializer(
            tweet,
            data=request.data,
            partial=True,
        )

        if tweetSerializer.is_valid():
            tweet = tweetSerializer.save()
            tweetSerializer = TweetDetailSerializer(tweet)
            return Response(
                {
                    "ok": True,
                    "data": tweetSerializer.data,
                },
                status=status.HTTP_200_OK,
            )
        else:
            return Response(
                {
                    "ok": False,
                    "error": tweetSerializer.errors,
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

    def delete(self, request, tweet_id):
        tweet = self.get_object(tweet_id)
        if tweet == "NotFound":
            return Response(
                {
                    "ok": False,
                    "error": f"No tweet with id : {tweet_id}",
                },
                status=status.HTTP_404_NOT_FOUND,
            )

        if not request.user.is_authenticated:
            return Response(
                {
                    "ok": False,
                    "error": "Please login first",
                },
                status=status.HTTP_401_UNAUTHORIZED,
            )

        if tweet.user != request.user:
            return Response(
                {
                    "ok": False,
                    "error": "You can only delete your own tweets",
                },
                status=status.HTTP_403_FORBIDDEN,
            )

        tweet.delete()
        return Response(
            {
                "ok": True,
                "data": "The Tweet is deleted successfully",
            },
            status=status.HTTP_200_OK,
        )
