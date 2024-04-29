from rest_framework.response import Response
from rest_framework.exceptions import NotFound
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
            }
        )

    def post(self, request):
        pass


# Get / Put / Delete
class TweetDetail(APIView):
    def get_object(self, tweet_id):
        try:
            return TweetModel.objects.get(id=tweet_id)
        except TweetModel.DoesNotExist:
            raise NotFound

    def get(self, request, tweet_id):
        serializer = TweetDetailSerializer(self.get_object(tweet_id))
        return Response(
            {
                "ok": True,
                "data": serializer.data,
            }
        )

    def put(self, request):
        pass

    def delete(self, request):
        pass
