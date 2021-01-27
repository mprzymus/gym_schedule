from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.generic import DetailView

from app.model.commands import NewExerciseUsage
from app.model.models import ExerciseUsage, Exercise
from app.views.user_access_service import can_user_perform
from app.views.views import dispatch_date


class ExerciseView(DetailView):
    template_name = 'app/exercise.html'
    model = ExerciseUsage

    def dispatch(self, request, *args, **kwargs):
        if can_user_perform(request.user, kwargs['usr_id']):
            return super(ExerciseView, self).dispatch(request, *args, **kwargs)
        return redirect(reverse('index'))

    def get_context_data(self, **kwargs):
        user = User.objects.filter(id=self.kwargs['usr_id']).get()
        day, month, year = dispatch_date(self.kwargs)
        context = super().get_context_data(**kwargs)
        context['all_exercises'] = Exercise.objects.all()
        context['submit'] = reverse('update_exercise', args=(year, month, day, self.kwargs['pk'], user.id))
        context['back'] = reverse('details', args=(year, month, day, user.id))
        return context


@login_required
def new_exercise_usage_view(request, **kwargs):
    day, month, year = dispatch_date(kwargs)
    user = User.objects.filter(id=kwargs['usr_id']).get()
    context = {
        'all_exercises': Exercise.objects.all(),
        'object': NewExerciseUsage(),
        'submit': reverse('update_exercise', args=(year, month, day, 0, user.id)),
        'back': reverse('details', args=(year, month, day, user.id))
    }
    return render(request, 'app/exercise.html', context=context)
