from django.contrib.auth.models import User
from django.db import models


class Exercise(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.CharField(max_length=1000)


class ExerciseUsage(models.Model):
    exercise_id = models.ForeignKey(Exercise, on_delete=models.CASCADE)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField()
    weight = models.FloatField(default=0)
    repetitions = models.IntegerField(default=0)
    sets = models.IntegerField(default=0)

    class Meta:
        unique_together = ["user_id", "date", "exercise_id"]
