import functools
from math import nan

from app.model.models import ExerciseUsage
from app.service.date_service import generate_dates_list
from io import StringIO

import matplotlib.pyplot as plt

from app.service.exercise_usage_service import find_exercises_for_day
from app.strings import *


class UserChartService:
    def __init__(self, user, period_start, period_end):
        self.user = user
        self.dates = generate_dates_list(period_start, period_end)

    def generate_chart_for_user(self):
        x, y = self.prepare_data()
        fig = plt.figure()
        plt.plot(x, y, linestyle="--", marker="o")
        plt.xticks(rotation=20)
        plt.title(GENERAL_CHART_TITLE)
        img_data = StringIO()
        fig.savefig(img_data, format='svg')
        img_data.seek(0)
        data = img_data.getvalue()
        return data

    def prepare_data(self):
        days = []
        data = []
        for day in self.dates:
            exercises = find_exercises_for_day(day, self.user)
            weight_sum = fold_left_exercises(exercises)
            if weight_sum != 0:
                days.append(day)
                data.append(weight_sum)
        return days, data


def fold_left_exercises(exercises):
    return functools.reduce(lambda acc, ex: ex.weight * ex.repetitions + acc, exercises, 0)
