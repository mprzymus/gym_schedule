from django.urls import path

from . import calendar_view

urlpatterns = [
    path('<int:year>/<int:month>/calendar', calendar_view.CalendarView.as_view(), name='calendar'),
]
