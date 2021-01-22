from django.test import TestCase

from app.model.models import ExerciseUsage
from app.service.user_stats_service import fold_left_exercises


class UserStatsTest(TestCase):

    def test_summing_exercises(self):
        ex1 = ExerciseUsage()
        ex1.weight = 5.0
        ex1.repetitions = 10

        ex2 = ExerciseUsage()
        ex2.weight = 2.5
        ex2.repetitions = 7

        ex3 = ExerciseUsage()
        ex3.weight = 50.0
        ex3.repetitions = 8

        should_be = ex1.weight * ex1.repetitions + ex2.weight * ex2.repetitions + ex3.weight * ex3.repetitions

        result = fold_left_exercises([ex1, ex2, ex3])

        self.assertEqual(should_be, result)
