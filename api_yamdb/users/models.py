from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    ROLE_CHOICES = (
        ("user", "User"),
        ("moderator", "Moderator"),
        ("admin", "Admin"),
    )

    role = models.CharField(
        max_length=10, choices=ROLE_CHOICES, default="user"
    )
    bio = models.TextField(
        "Биография",
        blank=True,
    )

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    def __str__(self) -> str:
        return self.username

    @property
    def is_admin(self):
        return self.role == "admin"

    @property
    def is_moderator(self):
        return self.role == "moderator"

    @property
    def is_user(self):
        return self.role == "user"
