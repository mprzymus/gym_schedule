import datetime
from io import StringIO

import matplotlib.pyplot as plt
import numpy as np
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.shortcuts import render, redirect


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
        return redirect_to_current_month()
    else:
        return user_login(request)


def redirect_to_current_month():
    year, month = __get_current_month()
    return redirect('/%d/%d/calendar' % (year, month))


def user_login(request):
    if not request.user.is_authenticated:
        return render(request, 'app/login.html')
    else:
        return redirect_to_current_month()


def register(request):
    return render(request, 'app/registration.html')


def register_process(request):
    username = request.POST['login']
    password = request.POST['pass']
    name = request.POST['name']
    lastname = request.POST['lastname']
    mail = request.POST['mail']
    user = User.objects.get(username=username)
    if user is None:
        user = User.objects.create_user(username, mail, password)
        user.first_name = name
        user.last_name = lastname
        user.save()
        return redirect("/")
    else:
        return register(request)


def logout_user(request):
    logout(request)
    return redirect("/index")


def default_user_site(request):
    return redirect_to_current_month()


def return_graph():
    x = np.arange(0, np.pi * 3, .1)
    y = np.sin(x)

    fig = plt.figure()
    plt.plot(x, y)

    imgdata = StringIO()
    fig.savefig(imgdata, format='svg')
    imgdata.seek(0)

    data = imgdata.getvalue()
    return data


def chart_test(request):
    context = {'graph': return_graph()}
    return render(request, 'app/dashboard.html', context)
