from typing import List

from app.model.models import ExerciseUsage
from app.service.exercise_usage_service import find_exercises_for_day, add_usage


def copy_day(date_from, date_to, user):
    ExerciseUsage.objects.filter(user_id=user, date=date_to).delete()
    exercises: List[ExerciseUsage] = find_exercises_for_day(date_from, user)
    for exercise in exercises:
        add_usage(date_to, exercise.exercise_id.name, exercise.repetitions, exercise.sets, exercise.weight, exercise.user_id)
