from django.db import models
from common.models import CommonModel


class Tweet(CommonModel):
    payload = models.TextField(max_length=180)
    user = models.ForeignKey(
        "users.User",
        on_delete=models.CASCADE,
    )

    def like_count(self):
        return self.likes.count()

    def __str__(self):
        return f"{self.user.name}'s Tweet : {self.payload[:10]} ..."

    class Meta:
        verbose_name_plural = "Tweets"


class Like(CommonModel):
    tweet = models.ForeignKey(
        "tweets.Tweet",
        on_delete=models.CASCADE,
        related_name="likes",
    )
    user = models.ForeignKey(
        "users.User",
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return f"{self.user.name}'s Like for Tweet : {self.tweet.payload[:10]} ..."

    class Meta:
        verbose_name_plural = "Likes"
