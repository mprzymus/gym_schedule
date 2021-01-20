from datetime import datetime

from django.contrib.auth.models import User
from django.test import TestCase

from app.model.models import Exercise, ExerciseUsage
from app.service.day_copy_service import copy_day
from app.service.exercise_usage_service import find_exercises_for_day


class DayCopyServiceTest(TestCase):
    exercise_name = "test"
    weight = 10
    repetition = 10
    sets = 3
    date = datetime(year=2021, month=1, day=15)
    date_future = datetime(year=2021, month=1, day=22)

    def setUp(self):
        self.user = User.objects.create_user('testUser', 'test@test.com', 'testpass')
        self.ex = Exercise(1, self.exercise_name)
        self.ex.save()
        usage = ExerciseUsage(id=1, user_id=self.user, exercise_id=self.ex, date=self.date, weight=self.weight,
                              repetitions=self.repetition, sets=self.sets)
        usage.save()

    def test_copy(self):

        copy_day(self.date, self.date_future, self.user)
        new_exercises = find_exercises_for_day(self.date_future, self.user)

        self.assertEqual(1, len(Exercise.objects.all()))
        self.assertEqual(1, len(new_exercises))

        new_object: ExerciseUsage = new_exercises[0]

        self.assertEqual(self.exercise_name, new_object.exercise_id.name)

    def test_should_clear_day_before_copy(self):
        ex = Exercise(2, "second")
        ex.save()
        usage = ExerciseUsage(id=2, user_id=self.user, exercise_id=ex, date=self.date_future, weight=self.weight,
                              repetitions=self.repetition, sets=self.sets)
        usage.save()

        copy_day(self.date, self.date_future, self.user)
        new_exercises = find_exercises_for_day(self.date_future, self.user)

        self.assertEqual(1, len(new_exercises))

    def test_not_delete_other_users_data(self):
        user2 = User.objects.create_user('testUser2', 'test@test.com', 'testpass')
        usage = ExerciseUsage(id=2, user_id=user2, exercise_id=self.ex, date=self.date_future, weight=self.weight,
                              repetitions=self.repetition, sets=self.sets)
        usage.save()

        copy_day(self.date, self.date_future, self.user)

        self.assertEqual(1, len(find_exercises_for_day(self.date_future, user2)))
