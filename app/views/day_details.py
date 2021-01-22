import datetime

from django.views import generic

from app.model.models import ExerciseUsage
from app.service.date_service import dispatch_date
from app.service.exercise_usage_service import exercise_usage_to_command


class DayDetails(generic.ListView):
    template_name = 'app/day_details.html'
    context_object_name = 'exercises'

    def get_queryset(self):
        date = self.get_date()
        exercises = ExerciseUsage.objects.filter(date=date, user_id=self.request.user)
        return map(exercise_usage_to_command, exercises)

    def get_date(self):
        day, month, year = dispatch_date(self.kwargs)
        month = month + 1
        return datetime.date(year, month, day)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        date = self.get_date()
        context['date'] = date.strftime("%d.%m.%Y")
        return context

