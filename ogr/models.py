from django.db import models
from django.utils import timezone
from django.contrib.auth import get_user_model
from datetime import date

# Create your models here.
class Friend(models.Model):
    user = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE)
    name = models.CharField(max_length=256)


class Ogr_ogr(models.Model):
    """金銭の貸し借りの記録"""
    user = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE)
    date = models.DateField(default=date.today())
    friends_name = models.ForeignKey(
        Friend,
        on_delete=models.CASCADE)
    title = models.CharField(max_length=256)
    money = models.IntegerField(default=0)
    detail = models.TextField(default='')
    solution = models.IntegerField(default=0) #未解決は0,解決済みは1


    