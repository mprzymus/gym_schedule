from django.contrib.auth.decorators import login_required
from django.urls import path

import app.views.account_management
from .views import views, calendar_view, day_details, exercise_view, account_management

urlpatterns = [
    path('<int:year>/<int:month>/calendar', login_required(calendar_view.CalendarView.as_view()), name='calendar'),
    path('<int:year>/<int:month>/<int:day>/details', login_required(day_details.DayDetails.as_view()), name='details'),
    path('login', app.views.account_management.user_login, name='login'),
    path('login_check', app.views.account_management.login_progress, name='login_check'),
    path('register', app.views.account_management.register, name='register'),
    path('register_process', app.views.account_management.register_process, name='register_process'),
    path('index', app.views.account_management.user_login, name='index'),
    path('', app.views.account_management.user_login, name='default'),
    path('logout', app.views.account_management.logout_user, name='logout'),
    path('<int:year>/<int:month>/<int:day>/details/<int:pk>', exercise_view.ExerciseView.as_view(),
         name='exercise_usage_details'),
    path('<int:year>/<int:month>/<int:day>/details/<int:pk>/delete', views.remove_usage, name='exercise_usage_remove'),
    path('<int:year>/<int:month>/<int:day>/new', exercise_view.new_exercise_usage_view, name='exercise_usage_new'),
    path('<int:year>/<int:month>/<int:day>/details/<int:pk>/update', views.update, name='update_exercise'),
    path('chart', views.chart_test, name='chart'),
]
