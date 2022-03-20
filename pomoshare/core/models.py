from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from datetime import timedelta
# from PIL import Image


class ModifiedUserModel(AbstractUser):
    def __str__(self):
        return self.username

    @property   
    def get_fullname(self):
        return f"{self.first_name} {self.last_name}"
    
    @property
    def get_streak(self):
        total_streak = 0
        run = True
        today = timezone.now().replace(hour=0, minute=0, second=0)
        yesterday = today - timedelta(days=1)
        while run:
            post = Post.objects.filter(completed_by = self).filter(completion_date__range = [yesterday, today]).exists()
            if post:
                today = yesterday
                yesterday = yesterday - timedelta(days=1)
                total_streak += 1
            else:
                run = False
        return total_streak


class Profile(models.Model):
    profile_of = models.OneToOneField(ModifiedUserModel, on_delete=models.CASCADE)
    country = models.CharField(max_length=200, blank=True, null=True)
    age = models.CharField(max_length=200, blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=300, blank=True, null=True)
    image = models.ImageField(default=None, upload_to='profile pictures/')
    friends = models.ManyToManyField(ModifiedUserModel, blank=True, related_name="friends")

    def __str__(self):
        return self.profile_of.username

    # def save(self, *args, **kwargs):
    #     super().save(*args, **kwargs)
    #     img = Image.open(self.image.path)
    #     if img.height > 400 or img.width > 400:
    #         img


    def get_friends(self):
        return self.friends.all()
    
    def get_friends_no(self):
        return self.friends.count()

    @property
    def get_full_name(self):
        return f"{self.profile_of.first_name} {self.profile_of.last_name}"


class FriendRequest(models.Model):
    sender = models.ForeignKey(ModifiedUserModel, on_delete=models.CASCADE, related_name='sender')
    receiver = models.ForeignKey(ModifiedUserModel, on_delete=models.CASCADE, related_name='receiver')
    accepted = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Friends: {self.friend_one.username} and {self.friend_two.username}"


class Notification(models.Model):
    receiver = models.ForeignKey(ModifiedUserModel, on_delete=models.CASCADE, related_name='notification_receiver')
    content = models.CharField(max_length=400, blank=False, null=False)

    def __str__(self):
        return f"{self.receiver} : {self.content}"


class BlockedWebsites(models.Model):
    blocked_by = models.ForeignKey(ModifiedUserModel, on_delete=models.CASCADE, related_name='sites')
    blocked_site = models.CharField(max_length=200)

    def __str__(self):
        return f"By: {self.blocked_by.username}. Site: {self.blocked_site}"


class Post(models.Model):
    completed_by = models.ForeignKey(ModifiedUserModel, on_delete=models.CASCADE, related_name='posts')
    completion_date = models.DateTimeField(auto_now_add=True, blank=False)
    time_in_seconds = models.IntegerField(blank=False, null=False)
    task = models.CharField(max_length=100, blank=False, null=False)
    likes = models.ManyToManyField(ModifiedUserModel, blank=True, related_name='likes')

    def __str__(self):
        return f"Task added on: {self.completion_date}"

    def liked(self, user):
        if user in self.likes.all():
            return True
        return False

    @property
    def like_count(self):
        count = self.likes.count()
        return f"{count} like" if count <= 1 else f"{count} likes"

    @property
    def comment_count(self):
        return self.comments.count()

    @property
    def all_comments(self):
        return self.comments.all()

    @property
    def time_in_minutes(self):
        return int(self.time_in_seconds / 60)

    @property
    def get_full_name(self):
        return f"{self.completed_by.first_name} {self.completed_by.last_name}"

    @property
    def get_username(self):
        return self.completed_by.username

    @property
    def posted_time(self):
        now = timezone.now()
        date_posted = self.completion_date
        time_difference = (now - date_posted).total_seconds()
        minutes = time_difference / 60
        hours = time_difference / 3600
        days = time_difference / 86400
        if (minutes < 1) and (hours < 1) and (days < 1):
            if int(time_difference) == 1:
                return f"{int(time_difference)} second"
            return f"{int(time_difference)} seconds"
        elif (minutes >= 1) and (hours < 1) and (days < 1):
            if int(minutes) == 1:
                return f"{int(minutes)} minute"
            return f"{int(minutes)} minutes"
        elif (hours >= 1) and (days < 1):
            if int(hours) == 1:
                return f"{int(hours)} hour"
            return f"{int(hours)} hours"
        elif days >= 1:
            if int(days) == 1:
                return f"{int(days)} day"
            return f"{int(days)} days"


class Comments(models.Model):
    comment = models.TextField(max_length=500, null=False)
    commented_by = models.ForeignKey(ModifiedUserModel, on_delete=models.CASCADE)
    comment_date = models.DateTimeField(auto_now_add=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')

    def __str__(self):
        return f"Task: {self.post.task}, " \
               f"Time taken: {self.post.time_in_seconds}, " \
               f"Commented by: {self.commented_by.username}"





