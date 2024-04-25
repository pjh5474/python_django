from django.urls import path
from . import views

urlpatterns = [
    path("", views.get_tweets),
    path("<int:tweet_id>", views.get_tweet),
]
