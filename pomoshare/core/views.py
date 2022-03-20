from multiprocessing import context
from django.shortcuts import render
from core.choices import hello, TASKS_DICT
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .models import ModifiedUserModel, Post, Profile, FriendRequest, Notification, Comments
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
        friend_list = user.profile.friends.prefetch_related().all()
        posts = Post.objects.filter(completed_by__in=friend_list).order_by('-completion_date').prefetch_related()
        context['posts'] = posts
        context['tasks'] = TASKS_DICT
        start_time = timezone.now().replace(hour=0, minute=0, second=0)
        context['leaderboard'] = ModifiedUserModel.objects.filter(posts__completion_date__gt=start_time).annotate(total_time=Sum('posts__time_in_seconds')).order_by('-total_time')[:3]
        # Calculating the follow count
        if user.friends.count() != None:
            context['friends'] = user.profile.friends.count()
        context['post_count'] = user.posts.count()
        if request.htmx:
            return render(request, 'partials/homepage/home-main.html', context)
        return render(request, 'pages/home.html', context)


def post_list(request):
    context = {}
    user = get_object_or_404(ModifiedUserModel, pk=request.user.pk)
    if user:
        profile = user.profile
        context['profile'] = profile
        friend_list = user.profile.friends.prefetch_related().all()
        posts = Post.objects.filter(completed_by__in=friend_list).order_by('-completion_date').prefetch_related()
        context['posts'] = posts
        context['tasks'] = TASKS_DICT
        # Calculating the follow count
        if request.htmx:
            return render(request, 'partials/homepage/post_list.html', context)



def post_details(request, id):
    post = Post.objects.prefetch_related('completed_by').get(pk=id)
    if post:
        id = id
        image = post.completed_by.profile.image.url
        username = post.get_username
        fullname = post.get_full_name
        firstname = fullname.split()[0]
        post_time = post.posted_time
        task_time = post.time_in_minutes
        task = post.task
        emoji = TASKS_DICT[task]
        user = request.user
        comments = post.comments.all().order_by('-comment_date')
        comment_count = post.comments.count()
        like_count = post.likes.count()
        like_count = f"{like_count} likes" if like_count >1 else f"{like_count} like"
        context = ({'comments': comments, 'task_obj': post, 
                    'like_count': like_count, 'user': user,
                    'username': username, 'fullname': fullname,
                    'firstname': firstname, 'post_time': post_time,
                    'task_time': task_time, 'emoji':emoji,
                    'comment_count':comment_count, 'image': image, 'id': id})
        if request.htmx:
            return render(request, 'components/homepage/post-details/post-details.html', context)


def post_comment(request, id):
    post = get_object_or_404(Post, pk=id)
    if post:
        comment = request.POST.get('comment')
        print('comment')
        print(comment)
        user = request.user
        Comments.objects.create(comment=comment, commented_by=user, post = post)
        comments = post.comments.all().order_by('-comment_date')
        context = {'comments':comments}
        if request.htmx:
            return render(request, 'components/homepage/post-details/post-comment-wrapper.html', context)


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


def like_unlike(request, pk):
    print("Received the request.")
    user = request.user
    post_id = pk
    post = Post.objects.get(pk=post_id)
    print("Got the post.")
    if user in post.likes.all():
        post.likes.remove(user)
    else:
        post.likes.add(user)
    like_count = post.likes.count()
    context = {'id': post_id, 'task_obj':post, 'user':request.user}
    context['likes'] = f"{like_count} likes" if like_count > 1 else f"{like_count} like"
    if request.htmx:
        return render(request, 'components/wrappers/like-btn-wrapper.html', context)


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



