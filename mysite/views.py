import time

from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_protect
from data import notebook


def index(request):
    languages = notebook.get_languages()
    return render(request, 'index.html', locals())


def edit(request):
    return render(request, 'edit.html')


@csrf_protect
def crud(request):
    utctime = str(int(time.time()))
    print(time.time())
    if request.method == "POST":
        language = request.POST.get('language')
        noteClass = request.POST.get('class')
        title = request.POST.get('title')
        describe = request.POST.get('describe')
        code = request.POST.get('code')
        note = {"language": language, "class": noteClass, "title": title, "describe": describe, "code": code,
                "time": utctime}
        rel = notebook.add_note(note)

    return render(request, 'edit.html')


@csrf_protect
def list(request, lan='Python'):
    languages = notebook.get_languages()
    classes = notebook.get_classes(lan)
    cla = request.GET.get('class')
    notes = notebook.get_list(lan, cla=cla)

    return render(request, 'list.html', locals())


def delete(request, id="2"):
    languages = notebook.get_languages()
    classes = notebook.get_classes("Python")
    notes = notebook.get_list("Python", cla=None)

    cla = request.GET.get('class')
    rel = notebook.del_note(id)
    if rel:
        print("ok")
    else:
        print("error")

    return render(request, 'list.html', locals())



@csrf_protect
def search(request):
    if request.method == "POST":
        text = request.POST.get('text')
        languages = notebook.get_languages()
        notes = notebook.search(text)

    return render(request, 'search.html', locals())
