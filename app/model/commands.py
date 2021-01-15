from app.model.models import ExerciseUsage


class ExerciseUsageCommand:
    def __init__(self, usage_id, exercise_name, date, weight=0, repetitions=0, sets=0):
        self.id = usage_id
        self.exercise_name = exercise_name
        self.date = date
        self.weight = weight
        self.repetitions = repetitions
        self.sets = sets

    @classmethod
    def from_exercise_usage(cls, exercise_name, exercise: ExerciseUsage):
        return cls(exercise.id, exercise_name, exercise.date, exercise.weight, exercise.repetitions, exercise.sets)


class NewExerciseUsage:
    def __init__(self):
        self.id = 0
