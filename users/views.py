from rest_framework.response import Response
from rest_framework.decorators import api_view
from .serializers import UserTweetsSerializer
from .models import User


@api_view()
def userTweets(request, user_id):
    try:
        user = User.objects.filter(id=user_id).get()
        serializer = UserTweetsSerializer(
            user,
        )
        return Response(
            {
                "ok": True,
                "data": serializer.data,
            }
        )

    except User.DoesNotExist:
        return Response(
            {
                "ok": False,
                "data": f"There is no User with id : {user_id}",
            }
        )
