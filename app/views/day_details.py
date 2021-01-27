import datetime

from django.contrib.auth.models import User
from django.shortcuts import redirect
from django.urls import reverse
from django.views import generic

from app.model.models import ExerciseUsage
from app.service.date_service import dispatch_date
from app.service.exercise_usage_service import exercise_usage_to_command
from app.views.user_access_service import can_user_perform


class DayDetails(generic.ListView):
    template_name = 'app/day_details.html'
    context_object_name = 'exercises'

    def dispatch(self, request, *args, **kwargs):
        if can_user_perform(request.user, kwargs['usr_id']):
            return super(DayDetails, self).dispatch(request, *args, **kwargs)
        return redirect(reverse('index'))

    def get_queryset(self):
        date = self.get_date()
        user = User.objects.filter(id=self.kwargs['usr_id']).get()
        exercises = ExerciseUsage.objects.filter(date=date, user_id=user)
        return map(exercise_usage_to_command, exercises)

    def get_date(self):
        day, month, year = dispatch_date(self.kwargs)
        month = month
        return datetime.date(year, month, day)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        day, month, year = dispatch_date(self.kwargs)
        date = self.get_date()
        user_id = self.kwargs['usr_id']
        context['date'] = date.strftime("%d.%m.%Y")
        context['url_to_new'] = reverse('exercise_usage_new', args=(year, month, day, user_id))
        context['year'] = year
        context['month'] = month
        context['day'] = day
        context['usr_id'] = user_id
        return context

