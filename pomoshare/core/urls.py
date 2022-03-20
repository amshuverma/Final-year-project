from django.urls import path
from .views import (homepage, leaderboard, friends, 
                    unfriend, search_friends, like_unlike, 
                    post_details, post_list, post_comment)
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', homepage, name="homepage"),
    path('post/all/', post_list, name="post_list"),
    path('post/<int:pk>/like', like_unlike, name="like unlike"),
    path('post/<int:id>/comment', post_comment, name="post comment"),
    path('post/<int:id>', post_details, name="post details"),


    path('leaderboard/', leaderboard, name="leaderboard"),
    path('leaderboard/<str:country>', leaderboard, name="leaderboard"),


    path('friends/', friends, name="friends"),
    path('friends/search/', search_friends, name="search-friends"),
    path('unfriend/<int:pk>', unfriend, name="unfriend"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)