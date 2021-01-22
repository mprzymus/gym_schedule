from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.shortcuts import redirect, render

from app.service.date_service import get_current_month


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
    today = get_current_month()
    return redirect('/%d/%d/calendar' % (today.year, today.month - 1))


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
