from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass


class Auction(models.Model):
    Time_left = models.IntegerField()
    Title = models.CharField(max_length=64)
    Category = models.CharField(max_length=12)
    Image = models.CharField(max_length=64)
    Description = models.CharField(max_length=100)
    Highest_Bid = models.IntegerField()
    Email = models.CharField(max_length=64, default = "die")
    Closed = models.CharField(max_length=5, null=True, blank=True)
    Highest_Bidder = models.CharField(max_length=64, default="wow")

    def __str__(self):
        return self.Title


class Comments(models.Model):
    page = models.CharField(max_length=30, null=True)
    content = models.CharField(max_length=100, default=None)

    def __str__(self):
        return self.page

class Checklist(models.Model):
    user = models.CharField(max_length=30, null=True)
    auction = models.CharField(max_length=100, default=None)

    def __str__(self):
        return self.title
