from django.db import models
from django.contrib.auth import get_user_model
import datetime

# Create your models here.
class Attendee(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=15,blank=True,null=True)
    user_id = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)


class Event(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    datetime = models.DateTimeField(auto_now_add=True)
    location = models.CharField(max_length=100)
    user_id = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)

    class Meta:
        ordering = ["-datetime"]

        

    