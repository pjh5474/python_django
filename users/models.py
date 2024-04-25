from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    """User Model"""

    class GenderChoices(models.TextChoices):
        MALE = ("male", "Male")
        FEMALE = ("female", "Female")
        Secret = ("secret", "Secret")

    class LanguageChoices(models.TextChoices):
        KR = ("kr", "Korean")
        EN = ("en", "English")

    first_name = models.CharField(
        editable=False,
        max_length=150,
    )
    last_name = models.CharField(
        editable=False,
        max_length=150,
    )
    name = models.CharField(max_length=150)
    gender = models.CharField(
        max_length=10,
        choices=GenderChoices.choices,
        default="secret",
    )
    language = models.CharField(
        max_length=2,
        choices=LanguageChoices.choices,
        default="kr",
    )

    def __str__(self):
        return self.name
