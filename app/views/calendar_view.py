from calendar import LocaleHTMLCalendar
import datetime

from django.urls import reverse
from django.utils.safestring import mark_safe
from django.views import generic

from ..service.coach_usage import did_request_coach, get_coach_mail
from ..service.exercise_usage_service import is_free_day
from ..strings import CONTACT_COACH, ASK_COACH

polish_locale = 'pl_PL.utf8'
polish_months = ['', 'styczeń', 'luty', 'marzec', 'kwiecień', 'maj', 'czerwiec', 'lipiec', 'sierpień', 'wrzesień',
                 'październik', 'listopad', 'grudzień']


class Calendar(LocaleHTMLCalendar):
    details_button = '<a href=\'%s/details\';">Szczegóły</a>'
    formatted_year, formatted_month = None, None

    def __init__(self, locale, user):
        super(Calendar, self).__init__(locale=locale)
        self.user = user

    def formatmonthname(self, theyear, themonth, withyear=True):
        if self.locale == polish_locale:
            header = '%s %d' % (polish_months[themonth], theyear)
            return '<tr><th colspan="7" class="month">%s</th></tr>' % header
        return super().formatmonthname(theyear, themonth, withyear)

    def formatday(self, day, weekday):
        if day == 0:
            return '<td class="%s">&nbsp;</td>' % self.cssclass_noday
        else:
            details_button = self.details_button % day
            css_day_class = 'day_off' if is_free_day(
                datetime.datetime(self.formatted_year, self.formatted_month, day), self.user) else "active_day"
            return '<td><span class="%s">%d</span><p>%s</p></td>' % (css_day_class, day, details_button)

    def formatmonth(self, theyear, themonth, withyear=True):
        self.formatted_month = themonth
        self.formatted_year = theyear
        v = []
        a = v.append
        a('<table border="1" cellpadding="0" cellspacing="0" class="%s">' % (
            self.cssclass_month))
        a('\n')
        a(self.formatmonthname(theyear, themonth, withyear=withyear))
        a('\n')
        a(self.formatweekheader())
        a('\n')
        for week in self.monthdays2calendar(theyear, themonth):
            a(self.formatweek(week))
            a('\n')
        a('</table>')
        a('\n')
        return ''.join(v)


class CalendarView(generic.TemplateView):
    template_name = 'app/schedule.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cal = Calendar('pl_PL.utf8', self.request.user)
        context['calendar'] = mark_safe(cal.formatmonth(self.kwargs['year'], self.kwargs['month'] + 1))
        next_month = (self.kwargs['month'] + 1) % 12
        context['nextMonth'] = next_month
        context['nextYear'] = self.kwargs['year'] + 1 if next_month == 0 else self.kwargs['year']
        previous_month = self.kwargs['month'] - 1
        switch_year = self.__is_year_switched(previous_month)
        context['previousMonth'] = 11 if switch_year else previous_month
        context['previousYear'] = self.kwargs['year'] - 1 if switch_year else self.kwargs['year']
        if did_request_coach(self.request.user):
            context['coach'] = 'mailto:' + get_coach_mail(self.request.user)
            context['coach_text'] = CONTACT_COACH
        else:
            context['coach'] = reverse('ask_coach')
            context['coach_text'] = ASK_COACH
        return context

    @staticmethod
    def __is_year_switched(previous_month):
        return previous_month < 0

    def get_queryset(self):
        pass
