from django.urls import path
from .views import homepage, leaderboard
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', homepage, name="homepage"),
    path('leaderboard/', leaderboard, name="leaderboard"),
    path('leaderboard/<str:country>', leaderboard, name="leaderboard")
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)