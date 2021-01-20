from datetime import datetime

from django.http import HttpResponseRedirect
from django.urls import reverse

from app.service.day_copy_service import copy_day


def copy_day_view(request, **kwargs):
    date = request.POST['date']
    date = datetime.strptime(date, "%Y-%m-%d")
    source_date = datetime.strptime(request.POST['source_date'], "%d.%m.%Y")
    copy_day(source_date, date, request.user)
    return HttpResponseRedirect(reverse('details', args=(source_date.year, source_date.month, source_date.day)))
