from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from .models import Auction
from .models import User
from .models import Comments
from .models import Checklist
import copy
import time

def index(request):
    auctions = Auction.objects.all()
    return render(request, "auctions/index.html", {
        "auctions": auctions
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
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


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
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")


def create(request):
    if "submit" in request.GET:
        if "Image" in request.GET:
            Image = request.GET["Image"]
        Title = request.GET["title"]
        Text = request.GET["text"]
        if "Category" in request.GET:
            Category = request.GET["Category"]
        Bid = request.GET["bid"]
        Auct = Auction.objects.create(Title=Title, Category=Category, Image=Image, Description=Text, Highest_Bid=Bid, Time_left=60, Email=request.user.email)
        Auct.save()
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/create.html")

def page(request, name):
    dont = True
    bids = list()
    commenties = list()
    chec = True
    tim = time.time()
    auctions = Auction.objects.all()
    for x in auctions:
        auction = x
        if x.Title == name:
            if x.Email == request.user.email:
                vendor = True
            else:
                vendor = False

            if request.user.is_authenticated:
                logged = True
            else:
                logged = False
            if "bid" in request.GET and request.GET["bid"] and not x.Closed:
                if x.Highest_Bid < int(request.GET["bid"]):
                    x.Highest_Bid = int(request.GET["bid"])
                    x.Highest_Bidder = request.user.email
                    x.save()
                    error = None
                else:
                    error = "Your Bid Must Be Greater Than The Current Winner's Bid"
                    tim = time.time()
            else:
                error = None

            for checks in Checklist.objects.all():
                if checks.auction == x.Title and checks.user == request.user.email:
                    dont = False
                    break
                else:
                    dont = True

            if "close" in request.GET:
                closed = "This Auction Is Closed"
                x.Closed = "True"
                if request.user.email == x.Highest_Bidder:
                    win = "Congrats! You Won This Auction!"
                    closed = None
                else:
                    win = None
                x.save()
            else:
                closed = False
                win = None
            if "lol" in request.GET and not x.Closed:
                for checks in Checklist.objects.all():
                    if checks.auction == x.Title and checks.user == request.user.email:
                        dont = False
                        break
                    else:
                        dont = True

                if dont:
                    check = Checklist.objects.create(user=request.user.email, auction=x.Title)
                    check.save()
                chec = True
            elif not dont:
                chec = True
            else:
                chec = False

            if "rem" in request.GET and not x.Closed:
                for checks in Checklist.objects.all():
                    if checks.auction == x.Title and checks.user == request.user.email:
                        checks.delete()
                chec = False
            if "comment" in request.GET:
                comments = Comments.objects.create(content=request.GET["comment"], page=x.Title)
                comments.save()
            for y in Comments.objects.all():
                if y.page == x.Title:
                    commenties.append(y)


            return render(request, "auctions/page.html", {
                "title" : name, "desc" : x.Description, "image" : x.Image,
                "type" : x.Category, "H_Bid" : x.Highest_Bid, "logged": logged, "vendor" : vendor ,"error" : error,
                "win" : win, "closed" : closed, "email" : x.Highest_Bidder, "comments": commenties, "check" : chec
            })
def wishlist(request):
    wish = list()
    auct = list()
    for x in Checklist.objects.all():
        if x.user == request.user.email:
            for auction in Auction.objects.all():
                if auction.Title == x.auction:
                    auct.append(auction)
            wish.append(x)
    return render(request, "auctions/wishlist.html", {
        "pages" : wish, "auction": auct
    })

def categories(request):
    categorie = dict()
    for x in Auction.objects.all():
        if x.Category not in categorie.keys() and not x.Closed:
            categorie[x.Category] = None
    for y in categorie.keys():
        matches = list()
        for z in Auction.objects.all():
            if z.Category == y and not z.Closed:
                matches.append(z)
        categorie[y] = matches
    return render(request, "auctions/categories.html",{
        "Categories": categorie
    })



