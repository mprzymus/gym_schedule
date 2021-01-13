from django.views.generic import DetailView

from app.model.models import ExerciseUsage


class ExerciseView(DetailView):
    template_name = 'app/exercise.html'
    model = ExerciseUsage
