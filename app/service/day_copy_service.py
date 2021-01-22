from datetime import date
from typing import List

import datetime as dt

from app.model.models import ExerciseUsage
from app.service.date_service import generate_dates_list
from app.service.exercise_usage_service import find_exercises_for_day, add_usage


def copy_day(date_from, date_to, user):
    clear_day(date_to, user)
    exercises: List[ExerciseUsage] = find_exercises_for_day(date_from, user)
    for exercise in exercises:
        add_usage(date_to, exercise.exercise_id.name, exercise.repetitions, exercise.sets, exercise.weight,
                  exercise.user_id)


def clear_day(date_to, user):
    ExerciseUsage.objects.filter(user_id=user, date=date_to).delete()


class PeriodCopier:
    min_repetitions: int
    max_repetitions: int
    repetitions_change = 0
    weight_up: float
    periods_to_change = 1

    def __init__(self, pattern_starts: date, pattern_length: int, copy_start: date, copy_end: date, user):
        self.pattern_starts = pattern_starts
        self.pattern_length = pattern_length
        self.copy_start = copy_start
        self.copy_end = copy_end
        self.user = user

    def generate_future_dates_list(self):
        return generate_dates_list(self.copy_start, self.copy_end)

    def generate_pattern_dates_list(self):
        last_pattern_day = self.pattern_starts + dt.timedelta(days=self.pattern_length - 1)
        return generate_dates_list(self.pattern_starts, last_pattern_day)

    def do_copy(self):
        i = 0
        dates = self.generate_future_dates_list()
        pattern_dates = self.generate_pattern_dates_list()
        for day in dates:
            source_date = pattern_dates[i % self.pattern_length]
            if self.periods_to_change > 0:
                period = int(i / self.pattern_length)
                current_repetition_change = int(period / self.periods_to_change) * self.repetitions_change
            else:
                current_repetition_change = 0
            self.copy_day(day, source_date, current_repetition_change)
            i = i + 1

    def copy_day(self, target_date, source_date, repetitions_to_add):
        exercises: List[ExerciseUsage] = find_exercises_for_day(source_date, self.user)
        clear_day(target_date, self.user)
        for exercise in exercises:
            exercise = self.add_step_to_exercise(exercise, repetitions_to_add)
            add_usage(target_date, exercise.exercise_id.name, exercise.repetitions, exercise.sets, exercise.weight,
                      exercise.user_id)

    def add_step_to_exercise(self, exercise: ExerciseUsage, repetitions_to_add) -> ExerciseUsage:
        exercise.repetitions = exercise.repetitions + repetitions_to_add
        while exercise.repetitions > self.max_repetitions:
            self.change_parameters(exercise)
        return exercise

    def change_parameters(self, exercise: ExerciseUsage):
        exercise.weight = exercise.weight + self.weight_up
        exercise.repetitions = exercise.repetitions - self.max_repetitions + self.min_repetitions - 1
