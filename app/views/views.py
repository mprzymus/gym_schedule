import datetime
from io import StringIO

import matplotlib.pyplot as plt
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

import app.service.exercise_usage_service as usage_service
from app.const import NEW_ELEMENT_PK
from app.service.date_service import dispatch_date


def return_graph():
    x = [1, 2, 3, 4, 5]
    y = [1, 5, 3, 2, 7]

    fig = plt.figure()
    plt.plot(x, y, linestyle="--", marker="o")

    imgdata = StringIO()
    fig.savefig(imgdata, format='svg')
    imgdata.seek(0)

    data = imgdata.getvalue()
    return data


def chart_test(request):
    context = {'graph': return_graph()}
    return render(request, 'app/dashboard.html', context)


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
