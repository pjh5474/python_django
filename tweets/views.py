from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import Tweet
from .serializers import TweetSerializer


@api_view()
def get_tweets(request):
    tweets = Tweet.objects.all()
    serializer = TweetSerializer(
        tweets,
        many=True,
    )
    return Response(
        {
            "ok": True,
            "data": serializer.data,
        }
    )


@api_view()
def get_tweet(request, tweet_id):
    try:
        tweet = Tweet.objects.filter(id=tweet_id).get()
        serializer = TweetSerializer(
            tweet,
        )
        return Response(
            {
                "ok": True,
                "data": serializer.data,
            }
        )
    except Tweet.DoesNotExist:
        return Response(
            {
                "ok": False,
                "data": f"There is no Tweet with id : {tweet_id}",
            }
        )
