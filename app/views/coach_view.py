from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.urls import reverse

from app.service.coach_service import is_coach
from app.service.coach_usage import get_coach_users, get_not_assigned_users, did_request_coach, get_user_coach, \
    assign_coach
from app.views.account_management import redirect_to_current_month


@login_required
def coach_index(request):
    coach = request.user
    if not is_coach(coach):
        return redirect_to_current_month()
    users = map(lambda relation: relation.user, get_coach_users(coach))
    new_users = map(lambda relation: relation.user, get_not_assigned_users())
    context = {
        'taken_users': users,
        'new_users': new_users,
    }
    return render(request, 'app/coach/index.html', context)


@login_required
def assign_user(request, **kwargs):
    coach = request.user
    if not is_coach(coach):
        return redirect_to_current_month()
    user_id = kwargs['id']
    user = User.objects.filter(id=user_id).get()
    if did_request_coach(user):
        relation = get_user_coach(user)
        assign_coach(relation, coach)
    return redirect(reverse('index'))
