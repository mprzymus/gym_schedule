from app.model.models import Exercise


def find_exercises_for_day(pk=0):
    return Exercise.objects.get(pk=pk)


def does_id_exist(pk=0):
    print(Exercise.objects.all())
    return Exercise.objects.filter(pk=pk).exists()
