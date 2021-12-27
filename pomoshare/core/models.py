from django.db import models
from django.contrib.auth.models import User
import datetime


class Profile(models.Model):
    profile = models.OneToOneField(User, on_delete=models.CASCADE)
    country = models.CharField(max_length=200, blank=True, null=True)
    age = models.CharField(max_length=200, blank=True, null=True)

    def __str__(self):
        return self.profile.username


class Task(models.Model):
    task_name = models.CharField(max_length=50)

    def __str__(self):
        return self.task_name


class Post(models.Model):
    task_completed_by = models.ForeignKey(Profile, on_delete=models.CASCADE)
    task_completion_date = models.DateTimeField(default=datetime.datetime.now(), blank=False)
    time = models.IntegerField(blank=False, null=False)
    task = models.ForeignKey(Task, on_delete=models.CASCADE)

    def __str__(self):
        return f"Task added on: {self.task_completion_date}"


