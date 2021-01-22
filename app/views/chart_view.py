from django.shortcuts import render
from django.views.generic.base import TemplateView

from app.const import POST_DATE_FORMAT
from app.service.date_service import get_time_boundaries, find_thirty_days_ago_and_today
from app.service.user_stats_service import UserChartService


class ChartView(TemplateView):
    template_name = 'app/dashboard.html'

    def post(self, request, *args, **kwargs):
        since, until = get_time_boundaries(request.POST)
        return self.create_charts(request, since, until)

    def get(self, request, *args, **kwargs):
        since, until = find_thirty_days_ago_and_today()
        return self.create_charts(request, since, until)

    def create_charts(self, request, since, until):
        service = UserChartService(request.user, since, until)
        context = {
            'graph': service.generate_chart_for_user(),
            'since': since.strftime(POST_DATE_FORMAT),
            'until': until.strftime(POST_DATE_FORMAT),
        }
        return render(request, self.template_name, context)
