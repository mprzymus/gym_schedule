from django.test import TestCase, Client


class CalendarTest(TestCase):
    client = Client()

    def test_january_date(self):
        response = self.client.get('/2020/00/calendar')
        self.assertEqual(200, response.status_code)
        self.assertEqual(1, response.context['nextMonth'])
        self.assertEqual(2020, response.context['nextYear'])
        self.assertEqual(11, response.context['previousMonth'])
        self.assertEqual(2019, response.context['previousYear'])

    def test_december_date(self):
        response = self.client.get('/2020/11/calendar')
        self.assertEqual(200, response.status_code)
        self.assertEqual(0, response.context['nextMonth'])
        self.assertEqual(2021, response.context['nextYear'])
        self.assertEqual(10, response.context['previousMonth'])
        self.assertEqual(2020, response.context['previousYear'])
