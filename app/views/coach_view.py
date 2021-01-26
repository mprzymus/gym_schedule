from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from app.service.coach_service import is_coach
from app.service.coach_usage import get_coach_users, get_not_assigned_users
from app.views.account_management import redirect_to_current_month


@login_required
def coach_index(request):
    coach = request.user
    if not is_coach(coach):
        return redirect_to_current_month()
    users = get_coach_users(coach)
    new_users = map(lambda relation: relation.user, get_not_assigned_users())
    context = {
        'taken_users': users,
        'new_users': new_users,
    }
    return render(request, 'app/coach/index.html', context)

