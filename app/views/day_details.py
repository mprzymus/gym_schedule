import datetime

from django.views import generic

from app.model.models import ExerciseUsage
from app.service.exercise_service import exercise_usage_to_command


class DayDetails(generic.ListView):
    template_name = 'app/day_details.html'
    context_object_name = 'exercises'

    def get_queryset(self):
        date = self.get_date()
        exercises = ExerciseUsage.objects.filter(date=date)
        return map(exercise_usage_to_command, exercises)

    def get_date(self):
        day = self.kwargs['day']
        month = self.kwargs['month'] + 1
        year = self.kwargs['year']
        return datetime.date(year, month, day)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        date = self.get_date()
        context['date'] = date.strftime("%d.%m.%Y")
        return context

