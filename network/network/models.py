from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    primary_key = True

class Followers(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    followers = list()

    def __str__(self):
        return self.user

class Posts(models.Model):
    title = models.CharField(max_length=20)
    content = models.CharField(max_length=100)
    user = models.CharField(max_length=30)
    likes = models.IntegerField()
    time = models.CharField(max_length=30)

    def __str__(self):
        return self.title

    class Meta:
        managed = True
