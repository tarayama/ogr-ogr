from django.db import models
from django.contrib.auth import get_user_model

# Create your models here.
class LineAccount(models.Model):
    user = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE)
    line_userid = models.CharField(max_length=256)
    line_nonceToken = models.CharField(max_length=256)

    def __str__(self):
        return self.line_userid
