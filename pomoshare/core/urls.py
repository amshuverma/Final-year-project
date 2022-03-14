from django.urls import path
from .views import homepage, leaderboard, friends, unfriend, search_friends
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', homepage, name="homepage"),
    path('leaderboard/', leaderboard, name="leaderboard"),
    path('leaderboard/<str:country>', leaderboard, name="leaderboard"),
    path('friends/', friends, name="friends"),
    path('friends/search/', search_friends, name="search-friends"),
    path('unfriend/<int:pk>', unfriend, name="unfriend"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)