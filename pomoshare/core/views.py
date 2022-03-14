from multiprocessing import context
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import ModifiedUserModel, Post, Profile, FriendRequest, Notification
from django.db.models import Sum, Aggregate, Q
from django.shortcuts import get_object_or_404
from django.utils import timezone
import datetime
import json


def homepage(request):
    context = {}
    user = get_object_or_404(ModifiedUserModel, pk=request.user.pk)
    if user:
        profile = user.profile
        context['profile'] = profile
        friend_list = user.profile.friends.all()
        posts = Post.objects.filter(completed_by__in=friend_list).order_by('-completion_date')
        context['posts'] = posts
        start_time = timezone.now().replace(hour=0, minute=0, second=0)
        context['leaderboard'] = ModifiedUserModel.objects.filter(posts__completion_date__gt=start_time).annotate(total_time=Sum('posts__time_in_seconds')).order_by('-total_time')[:3]
        # Calculating the follow count
        if user.friends.count() != None:
            context['friends'] = user.profile.friends.count()
        context['post_count'] = user.posts.count()
        if request.htmx:
            return render(request, 'partials/homepage/home-main.html', context)
        return render(request, 'pages/home.html', context)


def leaderboard(request, **kwargs):
    start_time = timezone.now().replace(hour=0, minute=0, second=0)
    country=kwargs.get('country')
    print(kwargs)
    if country:
        country = country
        qset = ModifiedUserModel.objects.filter(profile__country=country).filter(posts__completion_date__gt=start_time).annotate(total_time=Sum('posts__time_in_seconds')).order_by('-total_time')
    else:    
        qset = ModifiedUserModel.objects.filter(posts__completion_date__gt=start_time).annotate(total_time=Sum('posts__time_in_seconds')).order_by('-total_time')
    top_3 = qset[:3]
    others = qset[3:10]
    context = {'top_3':top_3, 'others':others, 'qset':qset}
    if request.htmx:
        return render(request, 'partials/homepage/leaderboard-main.html', context)
    return render(request, 'pages/leaderboard.html', context)


def friends(request):
    user = request.user
    people = ModifiedUserModel.objects.filter(profile__country=user.profile.country)
    context = {'people':people}
    result_type = "People you may know."
    context['result_type'] = result_type
    if request.htmx:
        return render(request, 'partials/homepage/friends.html', context)
    return render(request, 'pages/friends.html', context)


def search_friends(request):
    user = request.user
    keyword = request.POST.get("username")
    if request.htmx:
        if keyword == "":
            context["people"] = ModifiedUserModel.objects.filter(profile__country=user.profile.country)
            context["result_type"] = "People you may know"
        else:
            people = ModifiedUserModel.objects.filter(Q(first_name__icontains=keyword) | Q(last_name__icontains=keyword) | Q(profile__country__icontains=keyword))
            context = {"people":people, "result_type":"Search results"}
        return render(request, 'partials/homepage/friends-table.html', context)


def unfriend(request, pk):
    user = request.user
    friend = ModifiedUserModel.objects.get(pk=pk)
    if friend in user.profile.friends.all():
        user.profile.friends.remove(friend)
        return render(request, 'components/')


def send_friend_request(request, pk):
    sender = request.user
    receiver = ModifiedUserModel.objects.get(pk=pk)
    friend_request = FriendRequest(sender = sender, receiver = receiver)
    friend_request.save()
    notification_content = f"{sender.username} has sent you a friend request."
    notification = Notification(receiver=receiver, content=notification_content)


def accept_friend_request(request, pk):
    friend_request = FriendRequest.objects.get(pk=pk)
    friend_request.accepted = True
    friend_request.save()
    profile = Profile.objects.get(profile_of)



