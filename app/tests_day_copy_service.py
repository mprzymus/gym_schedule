from datetime import datetime

from django.contrib.auth.models import User
from django.test import TestCase

from app.model.models import Exercise, ExerciseUsage
from app.service.day_copy_service import copy_day, PeriodCopier
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


class PeriodCopierTest(TestCase):
    expected_size = 14

    def setUp(self) -> None:
        self.user = User.objects.create_user('testUser', 'test@test.com', 'testpass')
        start_date = datetime(year=2020, month=6, day=1)
        length = 7
        self.last_pattern_day = datetime(year=2020, month=6, day=length)
        self.copy_to = datetime(year=2020, month=6, day=8)
        self.copy_until = datetime(year=2020, month=6, day=21)
        self.copier = PeriodCopier(start_date, length, self.copy_to, self.copy_until, self.user)
        self.copier.max_repetitions = 12
        self.copier.min_repetitions = 8
        self.copier.weight_up = 2.5

    def test_period_generate(self):
        period = self.copier.generate_future_dates_list()

        self.assertEqual(self.expected_size, len(period))

        first = period[0]
        last = period[self.expected_size - 1]

        self.assertEqual(self.copy_to, first)
        self.assertEqual(self.copy_until, last)

    def test_pattern_dates_generate(self):
        dates = self.copier.generate_pattern_dates_list()

        first = dates[0]
        last = dates[self.copier.pattern_length - 1]

        first_should_be = self.copier.pattern_starts
        last_should_be = self.last_pattern_day

        self.assertEqual(self.copier.pattern_length, len(dates))
        self.assertEqual(first_should_be, first)
        self.assertEqual(last_should_be, last)

    def test_exercise_add(self):
        repetitions = self.copier.max_repetitions - 1
        weight = 10
        exercise = ExerciseUsage()
        exercise.repetitions = repetitions
        exercise.weight = weight

        result = self.copier.add_step_to_exercise(exercise, 1)

        self.assertEqual(repetitions + 1, result.repetitions)
        self.assertEqual(weight, result.weight)

    def test_exercise_add_one_weight_up(self):
        repetitions = self.copier.max_repetitions
        weight = 10
        exercise = ExerciseUsage()
        exercise.repetitions = repetitions
        exercise.weight = weight

        result = self.copier.add_step_to_exercise(exercise, 1)

        self.assertEqual(self.copier.min_repetitions, result.repetitions)
        self.assertEqual(weight + self.copier.weight_up, result.weight)

    def test_exercise_add_many_weight_up(self):
        repetitions = self.copier.max_repetitions
        weight = 10
        exercise = ExerciseUsage()
        exercise.repetitions = repetitions
        exercise.weight = weight

        result = self.copier.add_step_to_exercise(exercise, 9)

        self.assertEqual(11, result.repetitions)
        self.assertEqual(weight + 2 * self.copier.weight_up, result.weight)
