from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from .models import Posts as Post
from datetime import date
import datetime
from .models import Followers
from django.core.paginator import Paginator
import json
from django.http import JsonResponse


from .models import User


from django import template

register = template.Library()

@register.filter
def get_by_index(l, i):
    return l[i]

def compose(request):

    # Composing a new email must be via POS
    lol = ***REMOVED***
    hi
    # Check recipient emails
    data = json.loads(request.body)
    # Convert email addresses to users
    recipients = []

    # Get contents of email
    subject = data["title"]
    body = data["body"]

    # Create one email for each recipient, plus sender
    users = set()
    post = Post.objects.get(pk=data["id"]).content=body
    post.content=body
    post.title=subject
    post.save()
    return JsonResponse({"error": "Email not found."}, status=204)

def index(request, page, posts=None):
    ids = list()
    times = list()
    likes = list()
    if "AddT" in request.GET:
        newT = request.GET["AddT"]
        newC = request.GET["AddC"]
        today = date.today()
        # Textual month, day and year
        time = today.strftime("%B %d, %Y")

        new = Post.objects.create(title=newT, content=newC, user=request.user.username, likes=0, time=time)
        new.save()
        return HttpResponseRedirect("http://127.0.0.1:8000/index/1")
    pos = Post.objects.all()

    pos.reverse()
    pots = Paginator(pos, 10)
    pag = pots.page(page)
    pos = list(pag.object_list)

    for x in pos:
        ids.append(x.id)
        likes.append(x.likes)
        times.append(x.time)

    return render(request, "network/index.html", {
        "Posts": pos, "page": int(page), "next": pag.has_next(), "previous":pag.has_previous(), "before": int(page) - 1,
        "after": int(page) + 1, "numbers": range(9), "ids" :ids, "likes":likes, "times":times
    })


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect("http://127.0.0.1:8000/index/1")
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
            followers = Followers.objects.create(user=user)
            followers.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect("http://127.0.0.1:8000/index/1")
    else:
        return render(request, "network/register.html")


def profile(request, username):
    user = User(username=username)
    counter =0
    follower = Followers(user=user)
    followee = list()
    num1 = len(follower.followers)
    posts = Post.objects.filter(user=user.username)
    lol = Followers.objects.all()
    for x in lol:
        for y in x.followers:
            if user.username == y.username:
                followee.append(x.user)
                counter += 1
    if request.user not in follower.followers:
        if "follow" in request.GET:
            follower.followers.append(request.user)
            follow = "Unfollow"
            return HttpResponseRedirect(reverse("profile", kwargs={'username':username}))
        else:
            follow = "follow"

    else:
        follow = "unfollow"
        if "follow" in request.GET:
            follow = "follow"
            follower.followers.remove(request.user)
            return HttpResponseRedirect(reverse("profile", kwargs={'username':username}))

    return render(request, "network/profile.html", {
        "user" : user, "followers" : num1, "posts":
        posts, "follow" : follow, "following": len(followee)
    })

def following(request, username, page):

    lol = list()
    posts = list()
    followee = list()
    for x in Followers.objects.all():
        for y in x.followers:
            if username == y.username:
                followee.append(x.user)
                wow = Post.objects.filter(user=x.user)
                for j in wow:
                    posts.append(j)
    pots = Paginator(posts, 10)
    pag = pots.page(page)
    pos = pag.object_list
    return render(request, "network/index.html", {
        "Posts": posts, "page": int(page), "next": pag.has_next(), "previous": pag.has_previous(),
        "before": int(page) - 1, "user" : request.user,
        "after": int(page) + 1
    })





@csrf_exempt

def email(request, email_id):

    # Query for requested email
    # Composing a new email must be via POS
    # Check recipient emails
    data = json.loads(request.body)
    # Convert email addresses to users
    recipients = []

    # Get contents of email
    subject = data["subject"]
    body = data["body"]

    # Create one email for each recipient, plus sender
    users = set()
    lol = data["id"]
    ***REMOVED*** = data["recipients"]
    post = Post.objects.get(pk=lol)
    post.content = body
    post.title = subject
    post.save()
    return JsonResponse({"error": "Email not found."}, status=204)









