from django.urls import path
from .views import (blocked_sites_tab, friend_requests, homepage, leaderboard, friends, 
                    unfriend, search_friends, like_unlike, 
                    post_details, post_list, post_comment, get_pomodoro_time, pomodoro_complete,
                    friend_profile, send_friend_request, friend_requests, 
                    accept_friend_request ,register, login, all_posts, comment_delete, 
                    statistics, add_site, remove_site, timer_tab, blocked_sites_tab, sites_to_localstorage)
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('register/', register, name='register'),
    path('login', login, name='login'),

    path('', homepage, name="homepage"),
    path('post/all/', post_list, name="post_list"),
    path('post/<int:pk>/like', like_unlike, name="like unlike"),
    path('post/<int:id>/comment', post_comment, name="post comment"),
    path('post/<int:id>', post_details, name="post details"),
    path('post/comments/delete/', comment_delete, name="delete comment"),


    path('leaderboard/', leaderboard, name="leaderboard"),
    path('leaderboard/<str:country>', leaderboard, name="leaderboard"),


    path('friends/', friends, name="friends"),
    path('friends/search/', search_friends, name="search-friends"),
    path('unfriend/<int:pk>/', unfriend, name="unfriend"),
    path('add-friend/<int:pk>/', send_friend_request, name="send-request"),
    path('friends/accept/<int:pk>/', accept_friend_request, name="accept-request"),

    # path('profile/self/', profile, name="self profile"),
    path('profile/<int:pk>/', friend_profile, name="friend profile"),
    path('profile/friend-requests/<int:pk>/', friend_requests, name="friend requests"),
    path('profile/all-posts/<int:id>/', all_posts, name="all posts"),
    path('profile/statistics/', statistics, name="statistics"),

    path('block-website/add/', add_site, name="add site"),
    path('block-website/remove/<int:id>/', remove_site, name="remove site"),

    path('pomodoro/tabs/sites/', blocked_sites_tab, name="site tab"),
    path('pomodoro/tabs/clock/', timer_tab, name="timer tab"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

ajax_urlpatterns = [
    path('pomodoro/time/', get_pomodoro_time, name="pomodoro time"),
    path('pomodoro/completed/', pomodoro_complete, name="pomodoro complete"),
    path('get-blocked-websites/', sites_to_localstorage, name='sites to localstorage')
]

urlpatterns += ajax_urlpatterns