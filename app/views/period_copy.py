from django.views.generic import TemplateView


class PeriodCopyView(TemplateView):
    template_name = 'app/copy_period.html'