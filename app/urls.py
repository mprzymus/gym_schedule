from django.urls import path

from . import calendar_view, views

urlpatterns = [
    path('<int:year>/<int:month>/calendar', calendar_view.CalendarView.as_view(), name='calendar'),
    path('login', views.user_login, name='login'),
    path('login_check', views.login_progress, name='login_check'),
]
