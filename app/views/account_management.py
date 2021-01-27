from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.shortcuts import redirect, render
from django.urls import reverse

from app.service.coach_service import is_coach
from app.service.date_service import get_today


def login_progress(request):
    username = request.POST['login']
    password = request.POST['pass']
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        return redirect_by_role(user)
    else:
        return user_login(request)


def redirect_by_role(user):
    if not is_coach(user):
        return redirect_to_current_month(user)
    else:
        return redirect(reverse('coach_index'))


def redirect_to_current_month(usr):
    today = get_today()
    return redirect('/%d/%d/calendar/%d' % (today.year, today.month - 1, usr.id))


def user_login(request):
    if not request.user.is_authenticated:
        return render(request, 'app/login.html')
    else:
        return redirect_by_role(request.user)


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
    return redirect_to_current_month(request.user)
