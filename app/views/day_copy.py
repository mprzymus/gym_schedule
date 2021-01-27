from datetime import datetime

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.urls import reverse

from app.service.day_copy_service import copy_day
from app.const import POST_DATE_FORMAT
from app.views.user_access_service import can_user_perform


@login_required
def copy_day_view(request, **kwargs):
    user = User.objects.filter(id=kwargs['usr_id']).get()
    date = request.POST['date']
    source_date = datetime.strptime(request.POST['source_date'], "%d.%m.%Y")
    if can_user_perform(request.user, user.id):
        date = datetime.strptime(date, POST_DATE_FORMAT)
        copy_day(source_date, date, user)
    return HttpResponseRedirect(reverse('details', args=(source_date.year, source_date.month, source_date.day, user.id)))
