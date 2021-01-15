from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.urls import reverse
from django.views.generic import DetailView

from app.model.commands import NewExerciseUsage
from app.model.models import ExerciseUsage, Exercise
from app.views.views import dispatch_date


class ExerciseView(DetailView):
    template_name = 'app/exercise.html'
    model = ExerciseUsage

    def get_context_data(self, **kwargs):
        day, month, year = dispatch_date(self.kwargs)
        context = super().get_context_data(**kwargs)
        context['all_exercises'] = Exercise.objects.all()
        context['submit'] = reverse('update_exercise', args=(year, month, day, self.kwargs['pk']))
        return context


@login_required
def new_exercise_usage_view(request, **kwargs):
    day, month, year = dispatch_date(kwargs)

    context = {
        'all_exercises': Exercise.objects.all(),
        'object': NewExerciseUsage(),
        'submit': reverse('update_exercise', args=(year, month, day, 0))
    }
    return render(request, 'app/exercise.html', context=context)

