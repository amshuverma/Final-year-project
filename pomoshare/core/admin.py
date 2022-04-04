from django.contrib import admin
from django.contrib.auth.models import User
from .models import Profile, Post, ModifiedUserModel, Comments, FriendRequest

admin.site.register(ModifiedUserModel)
admin.site.register(Profile)
admin.site.register(Post)
admin.site.register(Comments)
admin.site.register(FriendRequest)

