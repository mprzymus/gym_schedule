import datetime

from django.http import HttpResponseRedirect
from django.urls import reverse

import app.service.exercise_usage_service as usage_service
from app.const import NEW_ELEMENT_PK
from app.service.date_service import dispatch_date


def update(request, **kwargs):
    exercise = request.POST['chosen_ex']
    repetitions = request.POST['repetitions']
    sets = request.POST['sets']
    weight = request.POST['weight']
    year = kwargs['year']
    month = kwargs['month']
    day = kwargs['day']
    pk = kwargs['pk']
    if pk == NEW_ELEMENT_PK:
        date = datetime.date(year, month + 1, day)
        db = usage_service.add_usage(date=date, exercise=exercise, repetitions=repetitions, sets=sets, weight=weight,
                                     user=request.user)
        pk = db.id
    else:
        usage_service.update(pk=pk, sets=sets, weight=weight, repetitions=repetitions, exercise=exercise)
    return HttpResponseRedirect(reverse('exercise_usage_details', args=(year, month, day, pk)))


def remove_usage(request, **kwargs):
    pk = kwargs['pk']
    day, month, year = dispatch_date(kwargs)
    usage_service.remove(pk)
    return HttpResponseRedirect(reverse('details', args=(year, month, day)))
