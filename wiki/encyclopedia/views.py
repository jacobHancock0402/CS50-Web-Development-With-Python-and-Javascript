from django.shortcuts import render

from . import util
import random

choices = ["CSS", "Django", "Git", "HTML", "Python"]
def index(request):

    if request.method == 'GET' and "q" in request.GET:
        query = request.GET['q']
    else:
        return render(request, "encyclopedia/index.html", {
            "entries": util.list_entries()
        })
    return search(request, query)



def get(request, nam):
    if request.method == 'GET' and "q" in request.GET:
        query = request.GET['q']
    else:
        return render(request, "encyclopedia/wik.html", {
            "entries" : util.get_entry(nam) , "title" : nam
        })
    return search(request,query)

def rand(request):
    choice = random.randint(0, 4)
    return render(request, "encyclopedia/wik.html", {
        "entries": util.get_entry(choices[choice])
    })

def search(request, query):
    results = list()
    for x in choices:
        if x.lower() == query.lower():
            return render(request, "encyclopedia/wik.html", {
                "entries": util.get_entry(x)
                          })

        elif query.lower() in x.lower():
            results.append(x)
    return render(request, "encyclopedia/results.html", {
        "entries": results
    })
def create(request):
     if request.method == 'GET' and "title" in request.GET:
         title = request.GET['title']
         text = request.GET['tex']
         texts = [title, text]
         wow = util.save_entry(title, text)

         return get(request, title)
     else:
         return render(request, "encyclopedia/create.html")

def edit(request, page):
    if request.method == 'GET' and "title" in request.GET:
        title = request.GET['title']
        text = request.GET['tex']
        texts = [title, text]
        wow = util.save_entry(page, text)
        return get(request, page)
    else:
        return render(request, "encyclopedia/Editing.html", {
            "entries": util.get_entry(page, html=False), "page":page
        })
def cap_title(page):
    title = list()
    counter = 0
    text = [util.get_entry(page, html=False)]
    for x in range(len(text)):
        if text[x] != '':
            title.append(text[x])
            text.remove(text[x])
        elif counter == 1:
            break
        else:
            counter = 1
    return [title,text]



