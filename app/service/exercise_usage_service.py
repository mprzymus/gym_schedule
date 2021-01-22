from app.model.commands import ExerciseUsageCommand
from app.model.models import ExerciseUsage
from app.service.exercise_service import get_or_create_exercise


def exercise_usage_to_command(exercise: ExerciseUsage):
    return ExerciseUsageCommand.from_exercise_usage(exercise.exercise_id.name, exercise)


def is_free_day(date, user):
    return len(find_exercises_for_day(date, user)) == 0


def find_exercises_for_day(date, user):
    return ExerciseUsage.objects.filter(date=date, user_id=user)


def add_usage(date, exercise, repetitions, sets, weight, user) -> ExerciseUsage:
    db_exercise = get_or_create_exercise(exercise)
    usage = ExerciseUsage(user_id=user, exercise_id=db_exercise, date=date, weight=weight, repetitions=repetitions,
                          sets=sets)
    usage.save()
    return usage


def update(pk, sets, weight, repetitions, exercise):
    db_exercise = get_or_create_exercise(exercise)
    usage = ExerciseUsage.objects.filter(pk=pk)
    usage.update(exercise_id=db_exercise, sets=sets, weight=weight, repetitions=repetitions)
    return usage


def remove(pk):
    ExerciseUsage.objects.get(pk=pk).delete()
