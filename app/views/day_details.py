import datetime

from django.views import generic

from app.model.models import ExerciseUsage


class DayDetails(generic.ListView):
    template_name = 'app/day_details.html'
    context_object_name = 'exercises'

    def get_queryset(self):
        user = self.request.user
        day = self.kwargs['day']
        month = self.kwargs['month'] + 1
        year = self.kwargs['year']
        print('%d %d %d' % (day, month, year))
        exercises = ExerciseUsage.objects.filter(date=datetime.datetime(year, month, day))
        return map(lambda ex: str(ex), exercises)

    def convert_to_command(self, exercise: ExerciseUsage):
        pass
