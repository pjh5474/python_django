from django.shortcuts import render
from .models import Tweet


# Create your views here.
def get_tweets(request):
    tweets = Tweet.objects.all()
    return render(
        request,
        "get_tweets.html",
        {
            "tweets": tweets,
            "title": "All Tweets",
        },
    )


def get_tweet(request, tweet_id):

    try:
        tweet = Tweet.objects.filter(id=tweet_id).get()
        return render(
            request,
            "get_tweet.html",
            {
                "tweet": tweet,
                "title": f"Tweet _ id : {tweet_id}",
            },
        )
    except Tweet.DoesNotExist:
        return render(
            request,
            "get_tweet.html",
            {
                "not_found": True,
            },
        )
