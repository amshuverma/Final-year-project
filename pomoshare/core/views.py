from turtle import title, width
import plotly.express as px
from django_countries import countries
from django.shortcuts import render, redirect
from core.choices import TASKS_DICT
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from .forms import NewUserCreationForm, UpdateProfileForm
from django.contrib.auth.forms import AuthenticationForm
from .models import BlockedWebsites, ModifiedUserModel, Post, FriendRequest, Notification, Comments
from django.db.models import Sum, Q
from django.shortcuts import get_object_or_404
from django.utils import timezone
from datetime import datetime, timedelta
import json


def register(request):
    if request.method == 'POST':
        form = NewUserCreationForm(request.POST)

        if form.is_valid():
            form.save()
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password1')
            user = authenticate(request, email = email, password = password)
            print(user)
            if user is not None:
                login(request, user)
            return redirect('homepage')

        context = {"form": NewUserCreationForm(request.POST)}
        return render(request, 'Authentication/register.html', context)

    context = {"form": NewUserCreationForm()}
    return render(request, 'Authentication/register.html', context)


def login_request(request):
    return render(request, 'Authentication/login.html')

@login_required
def homepage(request):
    context = {}
    user = request.user
    print(user.username)
    if user:
        profile = user.profile
        context['profile'] = profile
        friend_list = user.profile.friends.prefetch_related('friends').all()
        posts = Post.objects.filter(completed_by__in=friend_list).order_by('-completion_date').prefetch_related()
        context['posts'] = posts
        context['tasks'] = TASKS_DICT
        context['minutes'] = profile.pomodoro_minutes
        context['seconds'] = profile.pomodoro_seconds
        print(context['seconds'])
        start_time = timezone.now().replace(hour=0, minute=0, second=0)
        context['leaderboard'] = ModifiedUserModel.objects.filter(posts__completion_date__gt=start_time).annotate(total_time=Sum('posts__time_in_seconds')).order_by('-total_time')[:3]
        # Calculating the follow count
        if user.friends.count() != None:
            context['friends'] = user.profile.friends.count() - 1
        context['post_count'] = user.posts.count()
        if request.htmx:
            return render(request, 'partials/homepage/home-main.html', context)
        return render(request, 'pages/home.html', context)


def get_pomodoro_time(request):
    profile = request.user.profile
    if profile:
        minutes, seconds = profile.pomodoro_minutes, profile.pomodoro_seconds
        context = {'minutes': minutes, 'seconds': seconds}
        return JsonResponse(context)


def pomodoro_complete(request):
    user = request.user
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        Post.objects.create(completed_by = user, time_in_seconds = data['time'], task = data['task'])
        return JsonResponse({'Message':'Request successful'}, status=200)


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
        print(image)
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
        user = request.user
        if comment.strip() != "":
            Comments.objects.create(comment=comment, commented_by=user, post = post)
        comments = post.comments.all().order_by('-comment_date')
        context = {'comments':comments}
        if request.htmx:
            return render(request, 'components/homepage/post-details/post-comment-wrapper.html', context)


def add_site(request):
    site = request.POST.get('comment')
    site = site.strip().lower()
    user = request.user
    BlockedWebsites.objects.create(blocked_by = user, blocked_site = site)
    if request.htmx:
        blockedsites = user.sites.all()
        context={'blockedsites': blockedsites}
        return render(request, 'partials/homepage/container-block-websites.html', context)


def remove_site(request, id):
    site = get_object_or_404(BlockedWebsites, pk=id)
    user = request.user
    site.delete()
    if request.htmx:
        blockedsites = user.sites.all()
        context={'blockedsites': blockedsites}
        return render(request, 'partials/homepage/container-block-websites.html', context)


def blocked_sites_tab(request):
    user = request.user
    if request.htmx:
        blockedsites = user.sites.all()
        context={'blockedsites': blockedsites}
        return render(request, 'partials/homepage/blocked-websites.html', context)


def timer_tab(request):
    context={'tasks':TASKS_DICT}
    if request.htmx:
        return render(request, 'partials/homepage/clock.html', context)


def leaderboard(request, **kwargs):
    start_time = timezone.now().replace(hour=0, minute=0, second=0)
    country=kwargs.get('country')
    print(kwargs)
    if country:
        country = country
        qset = ModifiedUserModel.objects.filter(profile__country=country).filter(posts__completion_date__gt=start_time).annotate(total_time=Sum('posts__time_in_seconds')).order_by('-total_time')
        print(qset.query)
    else:    
        qset = ModifiedUserModel.objects.filter(posts__completion_date__gt=start_time).annotate(total_time=Sum('posts__time_in_seconds')).order_by('-total_time')
    top_3 = qset[:3]
    others = qset[3:10]
    context={'top_3': top_3, 'others': others}
    if request.htmx:
        return render(request, 'partials/homepage/leaderboard-main.html', context)
    return render(request, 'pages/leaderboard.html', context)


def friends(request):
    user = request.user
    people = ModifiedUserModel.objects.filter(profile__country=user.profile.country)
    if people:
        context = {'people':people}
        result_type = "People you may know."
        context['result_type'] = result_type
        if request.htmx:
            return render(request, 'partials/homepage/friends.html', context)
        return render(request, 'pages/friends.html', context)
    return render(request, 'pages/friends.html', context)


def search_friends(request):
    user = request.user
    keyword = request.POST.get("username")
    if request.htmx:
        if keyword.strip() == "":
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


# def profile(request):
#     user = request.user
#     posts = user.posts.all()
#     post_count = user.posts.count()
#     profile = user.profile
#     friends_count = user.profile.friends.count()
#     friend_requests_count = FriendRequest.objects.filter(receiver=user, accepted=False).count()
#     streak = user.get_streak
#     context={'user': user, 'posts': posts, 'profile': profile,
#             'post_count': post_count, 'friends_count': friends_count, 
#             'requests_count': friend_requests_count, 'streak': streak}
#     if request.htmx:
#         return render(request, 'partials/homepage/profile.html', context)
#     return render(request, 'pages/profile.html', context)


def friend_profile(request, pk):
    user = get_object_or_404(ModifiedUserModel, pk=pk)
    self_ = request.user
    form = UpdateProfileForm
    if user:
        if request.method == "POST":
            form = form(request.POST)
            if form.is_valid():
                self_.profile.status = form.cleaned_data['status']
                self_.profile.country = dict(countries)[form.cleaned_data['country']]
                self_.profile.save()
                return redirect('friend profile', pk)
        status = ''
        posts = user.posts.all()
        post_count = user.posts.count()
        profile = user.profile
        friends_count = user.profile.friends.count()
        friend_requests_count = FriendRequest.objects.filter(receiver=self_, accepted=False).count()
        streak = user.get_streak
        try:
            qset = Q((self_.receiver.filter(sender=user))|(self_.sender.filter(receiver=user)))
            obj = qset.children[0][0]
            if obj:
                status = 'friend' if obj.accepted else 'pending'
        except Exception as e:
            print(f"{e} was raised.")
            status = 'not friend'
        if self_ == user:
            status = 'self'
        context={'user': user, 'posts': posts, 'profile': profile, 'user_id':user.id,
            'post_count': post_count, 'friends_count': friends_count, 
            'streak': streak, 'status': status, 'requests_count':friend_requests_count, 'form': UpdateProfileForm}
        if request.htmx:
            return render(request, 'partials/homepage/profile.html', context)
        return render(request, 'pages/profile.html', context)



def unfriend(request, pk):
    self_ = request.user
    user = ModifiedUserModel.objects.get(pk=pk)
    self_.profile.friends.remove(user)
    user.profile.friends.remove(self_)
    try:
        qset = Q((self_.receiver.filter(sender=user))|(self_.sender.filter(receiver=user)))
        obj = qset.children[0][0]
        if obj:
            obj.delete()
    except Exception as e:
        print(f"Couldn't return user.")
    if request.htmx:
        return render(request, 'components/friend-add.html', {'id':user.id})
    

def send_friend_request(request, pk):
    receiver = get_object_or_404(ModifiedUserModel, pk=pk)
    sender = request.user
    if receiver:
        if request.htmx:
            FriendRequest.objects.create(sender=sender, receiver=receiver)
            notification_content = f"{sender.username} has sent you a friend request."
            notification = Notification(receiver=receiver, content=notification_content)
            notification.save()
            return render(request, 'components/friend-pending.html')


def friend_requests(request, pk):
    self_ = request.user
    profile_of = ModifiedUserModel.objects.get(pk=pk)
    if self_ == profile_of and request.htmx:
        context = {}
        friend_requests = FriendRequest.objects.filter(receiver=self_, accepted=False).prefetch_related('sender').prefetch_related('receiver')
        context['requests'] = friend_requests
        return render(request, 'partials/homepage/friend-requests.html', context)


def statistics(request):
    user = request.user
    time_vs_task_qset = user.posts.values('task').annotate(total_time=Sum('time_in_seconds')/60)
    fig = px.pie(
        names = [value['task'] for value in time_vs_task_qset],
        values = [value['total_time'] for value in time_vs_task_qset],
        color_discrete_sequence=px.colors.sequential.RdBu,
        title='Time spent in each task'
    )
    print(dir(fig))
    chart = fig.to_html()
    context = {'chart': chart}
    if request.htmx:
        return render(request, 'partials/homepage/statistics.html', context)


def all_posts(request, id):
    user = get_object_or_404(ModifiedUserModel, pk=id)
    posts = user.posts.all()
    context = {'posts': posts}
    if request.htmx:
        return render(request, 'partials/homepage/profile-posts.html', context)


def accept_friend_request(request, pk):
    friend_request = FriendRequest.objects.get(pk=pk)
    print(pk)
    self_ = request.user
    friend = friend_request.sender
    friend_request.accepted = True
    friend_request.save()
    friend.profile.friends.add(self_)
    self_.profile.friends.add(friend)
    if request.htmx:
        context = {}
        friend_requests = FriendRequest.objects.filter(receiver=self_, accepted=False).prefetch_related('sender').prefetch_related('receiver')
        context['requests'] = friend_requests
        return render(request, 'partials/homepage/friend-requests.html', context)


def comment_delete(request):
    data = json.loads(request.body)
    Comments.objects.get(pk=data['pk']).delete()
    return JsonResponse({'Success': 'True'}, status=200)


def sites_to_localstorage(request):
    user = request.user
    sites = user.sites.all()
    site_array = [site.blocked_site for site in sites]
    site_json = json.dumps(site_array)
    return JsonResponse({'data': site_json}, status=200)
    





