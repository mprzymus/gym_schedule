from django.db.models import QuerySet

from app.model.models import Exercise


def find_exercises_for_day(pk=0):
    return Exercise.objects.get(pk=pk)


def does_id_exist(pk=0):
    return Exercise.objects.filter(pk=pk).exists()


def get_by_name(name) -> QuerySet:
    return Exercise.objects.filter(name=name)


def add_exercise(name):
    ex = Exercise(name=name)
    ex.save()
    return ex


def get_or_create_exercise(exercise):
    db_exercise = get_by_name(exercise)
    if not db_exercise.exists():
        db_exercise = add_exercise(exercise)
    else:
        db_exercise = db_exercise.get()
    return db_exercise
