from django.contrib import admin
from .models import Tweet, Like
from .custom_filter import MuskFilter


@admin.register(Tweet)
class TweetAdmin(admin.ModelAdmin):
    list_display = (
        "payload",
        "user",
        "like_count",
        "created_at",
        "updated_at",
    )

    list_filter = (
        MuskFilter,
        "created_at",
        "updated_at",
    )

    readonly_fields = (
        "created_at",
        "updated_at",
    )

    search_fields = (
        "payload",
        "user__username",
    )


@admin.register(Like)
class LiekAdmin(admin.ModelAdmin):
    list_display = (
        "tweet",
        "user",
        "created_at",
        "updated_at",
    )

    list_filter = (
        "created_at",
        "updated_at",
    )

    readonly_fields = (
        "created_at",
        "updated_at",
    )

    search_fields = ("user__username",)
