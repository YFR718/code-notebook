import hashlib
import time

from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_protect
from data import notebook



def sha256(s):
    sha = hashlib.sha256()
    sha.update(s.encode("utf-8"))
    return sha.hexdigest()


def index(request):
    state = request.session.get('is_login',False)
    nums,words = notebook.get_statistic()

    return render(request, 'index.html',locals())


def edit(request, id=None):
    if not request.session.get('is_login',False):
        msg = "没有权限,请登录"
        return render(request, 'index.html', locals())
    else:
        state = True
    trans = ['\"',"\'","\\",'&']
    if id != None:
        note,codelist = notebook.get_a_note(id)
        codelen = len(note["code"])
        for i in range(codelen-1,-1,-1):
            if codelist[i] in trans:
                codelist.insert(i,"\\")
        note["code"] = "".join(codelist)
        print(note)

    return render(request, 'edit.html', locals())


@csrf_protect
def crud(request):
    if not request.session.get('is_login',False):
        msg = "没有权限,请登录"
        return render(request, 'index.html', locals())
    utctime = str(int(time.time()))
    if request.method == "POST":
        msg = "添加失败"
        language = request.POST.get('language')
        noteClass = request.POST.get('class')
        title = request.POST.get('title')
        describe = request.POST.get('describe')
        code = request.POST.get('code')
        note = {"language": language, "class": noteClass, "title": title, "describe": describe, "code": code,
                "time": utctime}

        rel = notebook.add_note(note)
        if rel:
            msg = "添加成功"

    return render(request, 'edit.html',locals())


@csrf_protect
def list(request, lan='Python'):
    state = request.session.get('is_login', False)
    languages = notebook.get_languages()
    classes = notebook.get_classes(lan)
    cla = request.GET.get('class')
    notes = notebook.get_list(lan, cla=cla)

    return render(request, 'list.html', locals())


def delete(request, id="-1"):
    if not request.session.get('is_login',False):
        msg = "没有权限,请登录"
        return render(request, 'index.html', locals())
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


def login(request):
    print("login")
    # 如果已经登录就直接返回主页
    if request.session.get('is_login', None):
        msg = "已登录!"
        state = True
        return render(request, 'index.html',locals())
    # 处理登录表单
    if request.method == "POST":
        # 获取登录信息
        cipher = request.POST.get('cipher', "")
        print(cipher)
        if sha256(cipher) == "fb6d483e0d3c704808dc7b42c3ec2d230c5fdebc70cfc0b255a391d6e1edbf98":
            request.session['is_login'] = True
            msg = "登录成功!"
            state = True
            print(msg)
            return render(request, 'index.html',locals())
        else:
            msg = "验证错误，请重新输入!"
            state = False

    # GET 请求直接返回登录页
    return render(request, 'index.html',locals())

def logout(request):
    request.session['is_login'] = False
    state = False
    msg = "退出成功!"
    print(msg)
    return render(request, 'index.html',locals())

def nav_bar(request):
    languages = notebook.get_languages()

    indexLan = ["Python", "Go", "Javascript", "HTML", "SQL"]

    context = {
        "languages": languages,
        "indexlan":indexLan

    }
    return context


def init(request):
    return request.session['is_login']