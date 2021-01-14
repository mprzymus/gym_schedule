from app.model.commands import ExerciseUsageCommand
from app.model.models import ExerciseUsage


def exercise_usage_to_command(exercise: ExerciseUsage):
    return ExerciseUsageCommand.from_exercise_usage(exercise.exercise_id.name, exercise)


def has_no_exercises(date):
    return len(find_exercises_for_day(date)) == 0


def find_exercises_for_day(date):
    return ExerciseUsage.objects.filter(date=date)

