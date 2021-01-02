import datetime

from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.http import HttpResponse


def __get_current_month():
    now = datetime.datetime.now()
    month = now.month - 1
    year = now.year
    return year, month


def login_progress(request):
    username = request.POST['login']
    password = request.POST['pass']
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        year, month = __get_current_month()
        return redirect('/%d/%d/calendar' % (year, month))
    else:
        return HttpResponse('nie ma')


def user_login(request):
    return render(request, 'app/login.html')
