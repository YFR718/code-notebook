import hashlib
import os.path
import time
from django.http import HttpResponse, StreamingHttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_protect
from data import notebook
from datetime import datetime



def sha256(s):
    sha = hashlib.sha256()
    sha.update(s.encode("utf-8"))
    return sha.hexdigest()


def index(request):
    state = request.session.get('is_login', False)
    return render(request, 'index.html', locals())


def edit(request, id=-1):
    if not request.session.get('is_login', False):
        msg = "没有权限,请登录"
        return render(request, 'index.html', locals())
    else:
        state = True
    trans = ['\"', "\'", "\\", '&']
    if id != -1:
        note, codelist = notebook.get_a_note(id)
        codelen = len(note["code"])
        for i in range(codelen - 1, -1, -1):
            if codelist[i] in trans:
                codelist.insert(i, "\\")
        note["code"] = "".join(codelist)
        print(note)

    return render(request, 'edit.html', locals())


@csrf_protect
def crud(request, id=-1):
    if not request.session.get('is_login', False):
        msg = "没有权限,请登录"
        return render(request, 'index.html', locals())
    utctime = str(int(time.time()))
    if request.method == "POST":
        language = request.POST.get('language')
        noteClass = request.POST.get('class')
        title = request.POST.get('title')
        describe = request.POST.get('describe')
        code = request.POST.get('code')
        note = {"language": language, "class": noteClass, "title": title, "describe": describe, "code": code,
                "time": utctime,"id":str(id)}
        print(id)
        if id=="-1":
            rel = notebook.add_note(note)
            if not rel:
                msg = "添加失败"
                return render(request, 'edit.html', locals())
            else:
                msg = "添加成功"
        else:
            rel = notebook.change_note(note)
            if not rel:
                msg = "更新失败"
                return render(request, 'edit.html', locals())
            else:
                msg = "更新成功"

    return render(request, 'edit.html', locals())


@csrf_protect
def list(request, lan='Python'):
    state = request.session.get('is_login', False)
    # languages = notebook.get_languages()
    classes = notebook.get_classes(lan)
    cla = request.GET.get('class')
    notes = notebook.get_list(lan, cla=cla)
    print(notes)

    return render(request, 'list.html', locals())


def delete(request, id="-1"):
    if not request.session.get('is_login', False):
        msg = "没有权限,请登录"
        return render(request, 'index.html', locals())
    # languages = notebook.get_languages()
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
        # languages = notebook.get_languages()
        notes = notebook.search(text)

    return render(request, 'search.html', locals())


def login(request):
    print("login")
    # 如果已经登录就直接返回主页
    if request.session.get('is_login', None):
        msg = "已登录!"
        state = True
        return render(request, 'index.html', locals())
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
            return render(request, 'index.html', locals())
        else:
            msg = "验证错误，请重新输入!"
            state = False

    # GET 请求直接返回登录页
    return render(request, 'index.html', locals())


def logout(request):
    request.session['is_login'] = False
    state = False
    msg = "退出成功!"
    print(msg)
    return render(request, 'index.html', locals())


def nav_bar(request):
    languages = notebook.get_languages()
    indexLan = ["Python", "Go", "Javascript", "HTML", "SQL","Java"]
    nums, lines = notebook.get_statistic()
    context = {
        "languages": languages,
        "indexlan": indexLan,
        "nums":nums,
        "lines":lines
    }
    return context


def down_chunk_file_manager(file_path, chuck_size=1024):
    """
    文件分片下发
    :param file_path:
    :param chuck_size:
    :return:
    """
    with open(file_path, "rb") as file:
        while True:
            chuck_stream = file.read(chuck_size)
            if chuck_stream:
                yield chuck_stream
            else:
                break


def download_md(request):
    if not request.session.get('is_login', False):
        msg = "没有权限,请登录"
        return render(request, 'index.html', locals())
    file = "code-notebook_"+str(datetime.date(datetime.today())) + ".md"
    path = os.path.join("mdbook", file)
    if not os.path.exists(path):
        data = notebook.get_all_note()
        t1 = ""
        t2 = ""
        with open(path, "x",encoding='utf-8') as f:
            for d in data:
                if d[1]!=t1:
                    t1=d[1]
                    f.write("# " + d[1] + "\n")
                if d[2]!=t2:
                    t2=d[2]
                    f.write("## " + d[2] + "\n")
                f.write("### " + d[3] + "\n")
                f.write("**" + d[4] + "**\n")
                f.write("```"+d[1]+'\n'+ d[5] + "\n```\n")
            f.write("123")
    response = StreamingHttpResponse(down_chunk_file_manager(path))
    response['Content-Type'] = 'application/octet-stream'
    response['Content-Disposition'] = 'attachment;filename="'+file+'"'
    return response

def download_database(request):
    if not request.session.get('is_login', False):
        msg = "没有权限,请登录"
        return render(request, 'index.html', locals())
    file_path = "database"
    response = StreamingHttpResponse(down_chunk_file_manager(file_path))
    response['Content-Type'] = 'application/octet-stream'
    response['Content-Disposition'] = 'attachment;filename="database.db"'
    return response


def init(request):
    return request.session['is_login']

def love(request,id):
    if not request.session.get('is_login', False):
        msg = "没有权限,请登录"
        return render(request, 'index.html', locals())
    l = notebook.love_note(id)

    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))



if __name__ == '__main__':
    file = str(datetime.date(datetime.today())) + ".md"
    path = os.path.join("../mdbook", file)
    print(path)
    if not os.path.exists(path):
        data = notebook.get_all_note("../database")

        print(2)
        with open(path, "x",encoding='utf-8') as f:
            for d in data:
                f.write("# " + d[1] + "\n")
                f.write("## " + d[2] + "\n")
                f.write("### " + d[3] + "\n")
                f.write("**" + d[4] + "**\n")
                f.write("```"+d[1]+'\n'+ d[5] + "\n```\n")
            f.write("123")
