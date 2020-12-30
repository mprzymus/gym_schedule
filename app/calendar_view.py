from calendar import LocaleHTMLCalendar

from django.utils.safestring import mark_safe
from django.views import generic

polish_locale = 'pl_PL.utf8'
polish_months = ['', 'styczeń', 'luty', 'marzec', 'kwiecień', 'maj', 'czerwiec', 'lipiec', 'sierpień', 'wrzesień',
                 'październik', 'listopad', 'grudzień']


class Calendar(LocaleHTMLCalendar):
    def __init__(self, locale):
        super(Calendar, self).__init__(locale=locale)

    def formatmonthname(self, theyear, themonth, withyear=True):
        if self.locale == polish_locale:
            header = '%s %d' % (polish_months[themonth], theyear)
            return '<tr><th colspan="7" class="month">%s</th></tr>' % header
        return super().formatmonthname(theyear, themonth, withyear)

    def formatday(self, day, weekday):
        if day == 0:
            return '<td class="%s">&nbsp;</td>' % self.cssclass_noday
        else:
            return '<td class="%s">%d</td>' % ('date', day)

    def formatmonth(self, theyear, themonth, withyear=True):
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


class CalendarView(generic.ListView):
    template_name = 'app/schedule.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cal = Calendar('pl_PL.utf8')
        context['calendar'] = mark_safe(cal.formatmonth(self.kwargs['year'], self.kwargs['month']))
        return context

    def get_queryset(self):
        pass
