from typing import Any
from django.contrib.admin import SimpleListFilter


class MuskFilter(SimpleListFilter):
    title = "Filter by Elon Musk"
    parameter_name = "Elon_Musk"

    def lookups(self, request, model_admin):
        return [
            ("contain", "with Elon Musk"),
            ("not_contain", "without Elon Musk"),
        ]

    def queryset(self, request: Any, tweets):
        parameter = self.value()
        if parameter:
            if parameter == "contain":
                return tweets.filter(payload__icontains="Elon Musk")
            elif parameter == "not_contain":
                return tweets.exclude(payload__icontains="Elon Musk")
            else:
                return tweets
        else:
            return tweets
