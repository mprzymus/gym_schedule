from django.contrib.auth.decorators import login_required
from django.urls import path

from .views import views, calendar_view, day_details

urlpatterns = [
    path('<int:year>/<int:month>/calendar', login_required(calendar_view.CalendarView.as_view()), name='calendar'),
    path('<int:year>/<int:month>/<int:day>/details', login_required(day_details.DayDetails.as_view()), name='details'),
    path('login', views.user_login, name='login'),
    path('login_check', views.login_progress, name='login_check'),
    path('register', views.register, name='register'),
    path('register_process', views.register_process, name='register_process'),
    path('index', views.user_login, name='index'),
    path('', views.user_login, name='default'),
    path('logout', views.logout_user, name='logout'),
    path('chart', views.chart_test, name='chart'),
]
