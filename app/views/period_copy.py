from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.views.generic.base import View
import datetime as dt
from app.const import POST_DATE_FORMAT
from app.service.day_copy_service import PeriodCopier
from app.views.user_access_service import can_user_perform


def create_copier(request, usr_id):
    user = User.objects.filter(id=usr_id).get()
    post = request.POST
    source_date = post['source_date']
    source_date: dt.date = dt.datetime.strptime(source_date, POST_DATE_FORMAT)
    period_length = int(post['period_length'])
    start_date = post['start_date']
    start_date = dt.datetime.strptime(start_date, POST_DATE_FORMAT)
    end_date = post['end_date']
    end_date = dt.datetime.strptime(end_date, POST_DATE_FORMAT)
    min_repetitions = int(post['min_rep'])
    max_repetitions = int(post['max_rep'])
    periods_to_change = int(post['periods_to_change'])
    weight_up = float(post['weight'])
    repetitions_change = int(post['repetitions_change'])
    copier = PeriodCopier(source_date, period_length, start_date, end_date, user)
    copier.min_repetitions = min_repetitions
    copier.max_repetitions = max_repetitions
    copier.weight_up = weight_up
    copier.periods_to_change = periods_to_change
    copier.repetitions_change = repetitions_change
    return copier


class PeriodCopyView(View):
    template_name = 'app/copy_period.html'

    def post(self, request, *args, **kwargs):
        if can_user_perform(request.user, kwargs['usr_id']):
            copier = create_copier(request, kwargs['usr_id'])
            copier.do_copy()
        return HttpResponseRedirect(reverse('index'))

    def get(self, request, *args, **kwargs):
        context = {'usr_id': kwargs['usr_id']}
        return render(request, self.template_name, context)
