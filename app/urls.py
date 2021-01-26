from django.contrib.auth.decorators import login_required
from django.urls import path

import app.views.account_management
from .views import views, calendar_view, day_details, exercise_view, account_management, day_copy, chart_view, \
    coach_view
from .views.period_copy import PeriodCopyView

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
    path('charts', login_required(chart_view.ChartView.as_view()), name='charts'),
    path('copy_day', day_copy.copy_day_view, name='copy'),
    path('copy_period', PeriodCopyView.as_view(), name='copy_period'),
    path('ask_coach', views.ask_for_coach, name='ask_coach'),
    path('coach/index', coach_view.coach_index, name='coach_index'),
    path('coach/assign/<int:id>', coach_view.assign_user, name='coach_assign'),
]
