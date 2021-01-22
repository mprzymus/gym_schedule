from datetime import datetime

from django.contrib.auth.models import User
from django.test import TestCase

from app.model.models import Exercise, ExerciseUsage
from app.service.exercise_usage_service import find_exercise_for_day_by_name


class ExerciseUsageServiceTest(TestCase):
    ex_name = "someName"
    date = datetime(year=2020, month=1, day=1)

    def setUp(self) -> None:
        self.user = User.objects.create_user('testUser', 'test@test.com', 'testpass')

        ex1 = Exercise()
        ex1.name = self.ex_name
        ex1.description = ' '
        ex1.save()

        self.ex_usage = ExerciseUsage()
        self.ex_usage.exercise_id = ex1
        self.ex_usage.user_id = self.user
        self.ex_usage.date = self.date
        self.ex_usage.save()

    def test_find_by_name(self):
        result = find_exercise_for_day_by_name(self.date, self.user, self.ex_name)

        self.assertEqual(1, len(result))
        self.assertEqual(self.ex_usage, result[0])

    def test_find_by_name_no_name(self):
        result = find_exercise_for_day_by_name(self.date, self.user, self.ex_name + 'notSameName')

        self.assertEqual(0, len(result))
