from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    pass


class Project(models.Model):

    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.CharField(max_length=1000)
    type = models.CharField(max_length=50)

    def __str__(self):
        return self.title
