from django.views.generic import DetailView

from app.model.models import ExerciseUsage, Exercise


class ExerciseView(DetailView):
    template_name = 'app/exercise.html'
    model = ExerciseUsage

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['all_exercises'] = Exercise.objects.all()
        return context
