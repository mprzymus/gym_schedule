from django.shortcuts import render
from django.views.generic.base import TemplateView

from app.const import POST_DATE_FORMAT
from app.model.models import Exercise
from app.service.date_service import get_time_boundaries, find_thirty_days_ago_and_today
from app.service.user_stats_service import UserChartService
from app.views.user_access_service import can_user_perform


class ChartView(TemplateView):
    template_name = 'app/dashboard.html'

    def post(self, request, *args, **kwargs):
        since, until = get_time_boundaries(request.POST)
        return self.create_charts(request, since, until)

    def get(self, request, *args, **kwargs):
        since, until = find_thirty_days_ago_and_today()
        return self.create_charts(request, since, until)

    def create_charts(self, request, since, until):
        service = self.create_service(request, since, until)
        if 'chosen_ex' in request.POST:
            chosen = request.POST['chosen_ex']
            ex_graph = service.generate_chart_for_exercise(chosen)
        else:
            ex_graph = ''
            chosen = ''
        context = {
            'graph': service.generate_general_chart(),
            'ex_graph': ex_graph,
            'since': since.strftime(POST_DATE_FORMAT),
            'until': until.strftime(POST_DATE_FORMAT),
            'all_exercises': Exercise.objects.all(),
            'object': chosen,
        }
        return render(request, self.template_name, context)

    def create_service(self, request, since, until):
        return UserChartService(request.user, since, until)


class CoachChartView(ChartView):
    def create_service(self, request, since, until):
        if can_user_perform(request.user, self.kwargs['usr_id']):
            return UserChartService(self.kwargs['usr_id'], since, until)
        else:
            return super(CoachChartView, self).create_service(request, since, until)
