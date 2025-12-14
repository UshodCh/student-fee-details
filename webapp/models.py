from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class student(models.Model):
    name=models.CharField(max_length=30)
    cls=models.IntegerField()
    reg=models.CharField(unique=True)
    fee=models.FloatField()