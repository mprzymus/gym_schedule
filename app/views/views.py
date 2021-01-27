import datetime

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.urls import reverse

import app.service.exercise_usage_service as usage_service
from app.const import NEW_ELEMENT_PK
from app.service.coach_usage import request_coach, did_request_coach
from app.service.date_service import dispatch_date
from app.views.user_access_service import can_user_perform


@login_required
def update(request, **kwargs):
    user = User.objects.filter(id=kwargs['usr_id']).get()
    year = kwargs['year']
    month = kwargs['month']
    day = kwargs['day']
    if can_user_perform(request.user, user.id):
        exercise = request.POST['chosen_ex']
        repetitions = request.POST['repetitions']
        sets = request.POST['sets']
        weight = request.POST['weight']
        pk = kwargs['pk']
        if pk == NEW_ELEMENT_PK:
            date = datetime.date(year, month, day)
            db = usage_service.add_usage(date=date, exercise=exercise, repetitions=repetitions, sets=sets, weight=weight,
                                         user=user)
            pk = db.id
        else:
            usage_service.update(pk=pk, sets=sets, weight=weight, repetitions=repetitions, exercise=exercise)
    return HttpResponseRedirect(reverse('exercise_usage_details', args=(year, month, day, pk, user.id)))


def remove_usage(request, **kwargs):
    day, month, year = dispatch_date(kwargs)
    user = User.objects.filter(id=kwargs['usr_id']).get()
    if can_user_perform(request.user, user.id):
        pk = kwargs['pk']
        usage_service.remove(pk)
    return HttpResponseRedirect(reverse('details', args=(year, month, day, user.id)))


@login_required
def ask_for_coach(request):
    if not did_request_coach(request.user):
        request_coach(request.user)
    return HttpResponseRedirect(reverse('index'))
