from datetime import datetime

from django.contrib.auth.models import User
from django.test import TestCase, Client

from app.model.models import ExerciseUsage, Exercise
from app.service.exercise_usage_service import exercise_usage_to_command
import app.service.exercise_service as ex_service


class CalendarTest(TestCase):
    client = Client()

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user('testUser', 'test@test.com', 'testpass')
        self.client.login(username="testUser", password="testpass")

    def test_january_date(self):
        response = self.client.get('/2020/00/calendar/1')
        self.assertEqual(200, response.status_code)
        self.assertEqual(1, response.context['nextMonth'])
        self.assertEqual(2020, response.context['nextYear'])
        self.assertEqual(11, response.context['previousMonth'])
        self.assertEqual(2019, response.context['previousYear'])

    def test_december_date(self):
        response = self.client.get('/2020/11/calendar/1')
        self.assertEqual(200, response.status_code)
        self.assertEqual(0, response.context['nextMonth'])
        self.assertEqual(2021, response.context['nextYear'])
        self.assertEqual(10, response.context['previousMonth'])
        self.assertEqual(2020, response.context['previousYear'])


class ExerciseUsageServiceTest(TestCase):
    exercise_name = "test"
    weight = 10
    repetition = 10
    sets = 3

    def setUp(self):
        self.user = User.objects.create_user('testUserService', 'test@test.com', 'testpass')

    def test_usage_to_command(self):
        ex = Exercise(1, self.exercise_name)
        date = datetime.now()
        usage = ExerciseUsage(id=1, user_id=self.user, exercise_id=ex, date=date, weight=self.weight,
                              repetitions=self.repetition, sets=self.sets)
        command = exercise_usage_to_command(usage)
        self.assertEqual(self.exercise_name, command.exercise_name)
        self.assertEqual(date, command.date)
        self.assertEqual(self.weight, command.weight)
        self.assertEqual(self.repetition, command.repetitions)
        self.assertEqual(self.sets, command.sets)


class ExerciseServiceTest(TestCase):
    def setUp(self) -> None:
        Exercise.objects.create(pk=1, name="name")

    def test_exists(self):
        result = ex_service.does_id_exist(pk=1)
        self.assertTrue(result)

    def test_not_exists(self):
        result = ex_service.does_id_exist(pk=-1)
        self.assertFalse(result)
